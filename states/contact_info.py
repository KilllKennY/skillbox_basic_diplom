from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    name = State()
    country = State()
    phone_number = State()
