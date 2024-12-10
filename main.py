import random
import psycopg2
import requests

from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup


print('Start telegram bot...')

state_storage = StateMemoryStorage()
token_bot = '7341178570:AAGclE8QP1ot1aEPZfJWx7OViA1hxI5G6eI'
bot = TeleBot(token_bot, state_storage=state_storage)

known_users = []

# Database connection settings
db_config = {
    'dbname': 'telegram_bot_english',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost'
}

def connect_db():
    return psycopg2.connect(**db_config)

def get_example_usage(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            example = data[0]['meanings'][0]['definitions'][0].get('example', 'Пример недоступен.')
            return example
        else:
            return 'Example not found.'
    except Exception as e:
        return 'Error fetching example.'

userStep = {}
buttons = []

def show_hint(*lines):
    return '\n'.join(lines)

def show_target(data):
    return f"{data['target_word']} -> {data['translate_word']}"

class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'

class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        known_users.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0

@bot.message_handler(commands=['cards', 'start'])
def next_cards_handler(message):
    cid = message.chat.id
    if cid not in known_users:
        known_users.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, "Hello, stranger, let study English...")
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    global buttons
    buttons = []

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT word_en, word_ru FROM Words WHERE word_en NOT IN (SELECT word_en FROM UserWords WHERE user_id = %s) ORDER BY RANDOM() LIMIT 1", (cid,))
        result = cur.fetchone()
        if result is None:
            bot.send_message(cid, "Все слова изучены. Добавьте новые слова, чтобы продолжить.")
            return
        target_word, translate = result
        example_usage = get_example_usage(target_word)
        cur.execute(
            "SELECT word_en FROM (SELECT DISTINCT word_en FROM Words WHERE word_en != %s) AS distinct_words ORDER BY RANDOM() LIMIT 3",
            (target_word,))
        others = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
    except Exception as e:
        bot.send_message(cid, f"Ошибка при получении данных из базы: {e}")
        return

    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}\nПример использования: {example_usage}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others

@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def process_next_command(message):
    next_cards_handler(message)

@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id
    userStep[cid] = 1
    bot.send_message(cid, "Введите слово на английском и перевод через запятую.")

@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word_handler(message):
    cid = message.chat.id
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT word_en FROM UserWords WHERE user_id = %s", (cid,))
        words = cur.fetchall()
        cur.close()
        conn.close()
        if not words:
            bot.send_message(cid, "Ваш словарь пуст.")
            return
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        for word in words:
            markup.add(types.KeyboardButton(word[0]))
        bot.send_message(cid, "Выберите слово для удаления:", reply_markup=markup)
        userStep[cid] = 2
    except Exception as e:
        bot.send_message(cid, f"Ошибка при получении списка слов: {e}")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    text = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    cid = message.chat.id
    if userStep.get(cid) == 1:
        try:
            word_en, word_ru = map(str.strip, text.split(','))
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO Users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING", (cid,))
            cur.execute("INSERT INTO UserWords (user_id, word_en, word_ru) VALUES (%s, %s, %s)",
                        (cid, word_en, word_ru))
            conn.commit()
            cur.close()
            conn.close()
            cur = connect_db().cursor()
            cur.execute("SELECT COUNT(*) FROM UserWords WHERE user_id = %s", (cid,))
            word_count = cur.fetchone()[0]
            bot.send_message(cid, f"Слово '{word_en}' добавлено с переводом '{word_ru}'! Теперь вы изучаете {word_count} слов.")
            userStep[cid] = 0
            next_cards_handler(message)
        except ValueError:
            bot.send_message(cid, "Ошибка! Введите слово и перевод через запятую, например: cat, кот.")
        except Exception as e:
            bot.send_message(cid, f"Ошибка при добавлении слова в базу данных: {e}")
        return
    elif userStep.get(cid) == 2:
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM UserWords WHERE user_id = %s AND word_en = %s", (cid, text))
            conn.commit()
            cur.close()
            conn.close()
            bot.send_message(cid, f"Слово '{text}' удалено из вашего словаря!")
            userStep[cid] = 0
            next_cards_handler(message)
        except Exception as e:
            bot.send_message(cid, f"Ошибка при удалении слова: {e}")
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data.get('target_word', None)
        correct_translate = data.get('translate_word', None)
        if target_word is None or correct_translate is None:
            bot.send_message(message.chat.id, "Ошибка: данные отсутствуют. Попробуйте снова.")
            next_cards_handler(message)
            return
        if text.strip().lower() == target_word.strip().lower():
            hint = "Отлично!❤ Нажмите 'Дальше', чтобы продолжить."
            next_btn = types.KeyboardButton(Command.NEXT)
            markup.add(next_btn)
            bot.send_message(message.chat.id, hint, reply_markup=markup)
        else:
            hint = "Неправильно, попробуйте еще раз."
            bot.send_message(message.chat.id, hint, reply_markup=markup)

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling(skip_pending=True)
