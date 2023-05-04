import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from telegram import ReplyKeyboardMarkup
import sqlite3

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

reply_keyboard = [['/schedule', '/news'],
                  ['/phone', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я ХайТек-бот. От меня ты узнаешь все о направлении Хайтек!",
        reply_markup=markup
    )


async def schedule(update, context):
    await update.message.reply_html(
        '''     НАУТИЛУС
        понедельник	16:10 - 17:40
        пятница 16:10 - 17:40
        
        ЖЕЛЕЗНЫЙ ЧЕЛОВЕК
        среда	16:10 - 17:40
        суббота	16:10 - 17:40
        
        ГЛАДОС
        понедельник	14:30 - 16:00
        пятница	14:30 - 16:00
        
        ОПТИМУС
        среда	17:50 - 19:20
        суббота	17:50 - 19:20
        
        ПОРТАЛ 
        вторник	16:10 - 17:40
        четверг	16:10 - 17:40
        
        НЕФАРИО 
        вторник	14:30 - 16:00
        четверг	14:30 - 16:00
        
        ЭНТЕРПРАЙЗ
        понедельник	17:50 - 19:20
        пятница	17:50 - 19:20''',
        reply_markup=markup
    )


async def news(update, context):
    con = sqlite3.connect('db/mydb.db')
    cur = con.cursor()
    result = cur.execute("""SELECT title, content FROM news ORDER BY created_date DESC""").fetchmany(5)
    print(result)
    mes = '\n\n'.join(['\n'.join(i) for i in result])
    await update.message.reply_html(mes)


async def phone(update, context):
    await update.message.reply_html("администратор\n+7 (918) 832-42-56\nпн-пт с 10 до 18 часов")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler('schedule', schedule))
    application.add_handler(CommandHandler('news', news))
    application.add_handler(CommandHandler('phone', phone))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
