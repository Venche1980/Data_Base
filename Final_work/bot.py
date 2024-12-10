# bot.py
from telebot import TeleBot, types
from telebot.storage import StateMemoryStorage
from handlers import register_handlers
from states import MyStates  # Import MyStates from states.py
from config import BOT_TOKEN

state_storage = StateMemoryStorage()
bot = TeleBot(BOT_TOKEN, state_storage=state_storage)

if __name__ == "__main__":
    register_handlers(bot)
    bot.infinity_polling(skip_pending=True)