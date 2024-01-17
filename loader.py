from telebot import TeleBot
from dotenv import load_dotenv
from config_data import config


load_dotenv()
bot = TeleBot(token=config.BOT_TOKEN)

print('Hello!')
