from flask import Flask, render_template, redirect
from data import db_session
from data.form.user import RegisterForm, LoginForm
from data.form.news import NewsForm
from data.users import User
from data.news import News
from flask_login import LoginManager, login_user, login_required, logout_user
from os import listdir



app = Flask(__name__)
app.config['SECRET_KEY'] = 'ruziegel_app'
login_manager = LoginManager()
login_manager.init_app(app)




def main():
    db_session.global_init("db/mydb.db")

    app.run(debug=True)



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/login
@app.route('/')
def index():
    photos = listdir('static/img/hitech_photos')
    return render_template('index.html', photos=photos, count_photos=len(photos))


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news')
def news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return render_template('news_list.html', news=news)


@app.route('/addnews', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        db_sess.add(news)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


if __name__ == '__main__':
    main()
