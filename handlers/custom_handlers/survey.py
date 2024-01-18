from loader import bot
from keyboards.reply.contact import request_contact
from states.contact_info import UserInfoState
from telebot.types import Message


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Здравтвуйте {message.from_user.username}, введите своё имя: ')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо, теперь укажите страну')
        bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'В имени не может быть цифр')


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id,
                         'Спасибо, теперь нажмите кнопку, чтобы отправить свои контакты',
                         reply_markup=request_contact()
                         )
        bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['country'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Название страны может быть только из букв.')


@bot.message_handler(content_type=['text', 'contact'], state=UserInfoState.phone_number)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            text = f'Спасибо за предоставленные данные: \n' \
                    f'Имя - {data["name"]} \n Страна - {data["country"]} ' \
                    f'\n Номер телефона - {data["phone_number"]}'

            bot.send_message(message.from_user.id, text, parse_mode=html)
    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить данные, нажмите кнопку.')
