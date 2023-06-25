import telebot
from telegram.ext import Updater, MessageHandler, filters


bot = telebot.TeleBot("6053282566:AAHVdAgIO5KfVyRcHIDbv98ZRsjwL01qp0Y",parse_mode=None)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message,"hello, how are you doing?")
    
@bot.message_handler(func=lambda m:True)
def echo_all(message):
    bot.reply_to(message, message.text)
    
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    echo_handler = MessageHandler(filters.text &amp; (~filters.command), echo)
    bot.dispatcher.add_handler(echo_handler)

    

bot.infinity_polling(none_stop = True)