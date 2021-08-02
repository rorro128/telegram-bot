import os, qrcode
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

INPUT_TEXT = 0

#FUNCION DEL SALUDO
def start(update, context):
    update.message.reply_text(
        text = 'hola rodrigo',
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Generar QR', callback_data='qr')],
            [InlineKeyboardButton(text='Sobre el autor', url='https://twitter.com/rorro128')]
        ])
    )

#INFORMACION DEL USUARIO
def getBotInfo(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user['first_name']
    print(context)
    bot.sendMessage(
        chat_id = chatId,
        parse_mode = 'HTML',
        text = f'Hola soy un bot creado por <b>Rodrigo Tardone</b>' 
    )

#MENSAJE DE BIENVENIDA AL GRUPO
def welcomeMsg(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    updateMsg = getattr(update, 'message', None)
    for user in updateMsg.new_chat_members:
        userName = user.first_name

    bot.sendMessage(
        chat_id = chatId,
        parse_mode = 'HTML',
        text = f'Bienvenido al grupo {userName}'
    )

#SOLICITA TEXTO PARA GENERAR QR
def qr_command_handler(update, context):
    update.message.reply_text('Enviame texto para generar QR')
    return INPUT_TEXT

def qr_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame texto para generar QR'
    )
    return INPUT_TEXT

#GENERA FOTO DEL CODIGO QR
def generate_qr(text):
    filename = text + '.jpg'
    img = qrcode.make(text)
    img.save(filename)
    return filename

#SUBE LA FOTO DEL QR GENERADO AL SERVIDOR DE TELEGRAM Y LA ENVIA AL USUARIO DEL CHAT
def send_qr(filename, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        photo=open(filename, 'rb')
    )
    os.unlink(filename)

def input_text(update, context):
    text = update.message.text
    
    filename = generate_qr(text)
    chat = update.message.chat
    #print(chat)
    send_qr(filename, chat)
    return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(token='', use_context=True)
    dp = updater.dispatcher

    #COMANDO INICIO BOT SALUDO
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('info', getBotInfo))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeMsg))
    
    #CAPTURA DE COMANDOS DE INTERACCION
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler),
            CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)
        ],
        states={
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
        },
        fallbacks=[]
    ))

    updater.start_polling() #ESTA PREGUNTANDO POR MENSAJES ENTRANTES
    updater.idle() #PERMITE CERRAR EL PROCESO CON CTRL+C
