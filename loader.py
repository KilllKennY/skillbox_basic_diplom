import os
from telebot import TeleBot
from dotenv import load_dotenv


load_dotenv()
bot = TeleBot(os.getenv('BOT_TOKEN'))
