from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from dotenv import load_dotenv
from config_data import config


load_dotenv()
storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=state)
