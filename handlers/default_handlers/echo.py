from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    bot.send_message(
        message.chat.id, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
    )
