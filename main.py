import telebot


bot = telebot.TeleBot("6053282566:AAHVdAgIO5KfVyRcHIDbv98ZRsjwL01qp0Y",parse_mode=None)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message,"hello, how are you doing?")
    
@bot.message_handler(func=lambda m:True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling(none_stop = True)