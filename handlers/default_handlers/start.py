from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    bot.send_message(message.chat.id, f'Hello, dear {message.from_user.full_name}')
