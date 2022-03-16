import telebot
from telebot import types
from datetime import date, datetime, timedelta
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from decouple import config
from loguru import logger



from database.user_bd import create_user_bd, set_user_info, get_user_info
from database.history_bd import create_history_bd, set_history_info, get_history_info, clear_history_bd
from radipid import find_destinations, output_lowprice_highprice, output_bestdeal


logger.add('log.log', format='{time}, {level}, {message}', level='INFO')
token = config('SECRET_KEY')
rapidapi_key = config('RAPIDAPI_KEY')
bot = telebot.TeleBot(token)


@logger.catch
@bot.message_handler(commands=['start'])
def start_handler(message: types.Message) -> None:
    """ Функция, выполняющая команду /start"""

    logger.info(f'User {message.chat.id} used command /start')
    bot.send_message(chat_id=message.chat.id,
                     text=f"Добрый день, {message.from_user.first_name}!")
    help_handler(message)


@logger.catch
@bot.message_handler(commands=['help'])
def help_handler(message: types.Message) -> None:
    """ Функция, выполняющая команду /help"""

    logger.info(f'User {message.chat.id} used command /help')
    bot.send_message(chat_id=message.chat.id,
                     text='Для работы бота, выбирайте одну из нижеперечисленных команд:\n'
                          '/lowprice - вывод самых дешевых отелей в городе;\n'
                          '/highprice - вывод самых доорогих отелей в городе;\n'
                          '/bestdeal - вывод отелей, наиболее подходящих по цене и расположению от центра;\n'
                          '/history - вывод истории поиска отелей;\n'
                          '/help - вызов перечня команд.')


@logger.catch
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def beginning(message: types.Message) -> None:
    """ Функция, которая выполняет команды /lowprice, /highprice, /bestdeal"""

    logger.info(f'User {message.chat.id} used command {message.text}')
    create_user_bd(message.chat.id)
    create_history_bd(message.chat.id)
    set_user_info(column='command', value=message.text, user_id=message.chat.id)
    bot.send_message(message.chat.id, text='В каком городе будем искать?')
    bot.register_next_step_handler(message=message, callback=get_city)


@logger.catch
def get_city(message: types.Message) -> None:
    """ Функция поиска города по запросу пользователя. Также подбирает подобные варианты."""

    destination = message.text
    suggestions = find_destinations(destination)
    while len(suggestions) == 0:
        bot.send_message(chat_id=message.chat.id, text='Такой город не найдем. Попробуйте еще раз.')
        bot.register_next_step_handler(message=message, callback=get_city)
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    for city, destination_id in suggestions.items():
        inline_button = types.InlineKeyboardButton(city, callback_data=destination_id)
        inline_keyboard.add(inline_button)
    inline_button = types.InlineKeyboardButton('Выбрать другой город', callback_data='123')
    inline_keyboard.add(inline_button)
    bot.send_message(chat_id=message.chat.id, text='Уточните название города:', reply_markup=inline_keyboard)


bot.polling(none_stop=True, interval=0)
