from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

#FUNCION DEL SALUDO
def start(update, context):
    button1 = InlineKeyboardButton(
        text = 'Sobre el autor',
        url = 'https://es.cointelegraph.com/'
    )
    button2 = InlineKeyboardButton(
        text = 'Perfil Twitter',
        url = 'https://twitter.com/rorro128'
    )
    update.message.reply_text(
        text = 'haz click en un boton',
        reply_markup=InlineKeyboardMarkup([
            [button1,button2]
        ])
    )

if __name__ == '__main__':
    updater = Updater(token='', use_context=True)
    dp = updater.dispatcher

    #COMANDO INICIO BOT SALUDO
    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()