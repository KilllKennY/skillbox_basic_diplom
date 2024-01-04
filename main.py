import telebot
from telebot import types


token = '5117555538:AAFs3lXGx8ilgAitAdbQxze_Ugp2rKDRb5I'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello!')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Кнопка":
        bot.send_message(message.chat.id, 'https://magnetic-evergreen-187.notion.site/'
                                          'Python-Basic-3ac614e60b7e434e9d9c018023319c04')


bot.infinity_polling()
