# handlers.py
from telebot import types
from database import fetch_word, fetch_random_words, insert_user_word, delete_user_word, connect_db
from api import get_example_usage
from states import MyStates  # Import MyStates from states.py

COMMANDS = {
    'ADD_WORD': 'Добавить слово ➕',
    'DELETE_WORD': 'Удалить слово🔙',
    'NEXT': 'Дальше ⏭'
}

user_step = {}


def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_handler(message):
        cid = message.chat.id
        # Отправка приветственного сообщения
        bot.send_message(
            cid,
            "Привет 👋 Давай попрактикуемся в английском языке. Тренировки можешь проходить в удобном для себя темпе.\n"
            "Причём у тебя есть возможность использовать тренажёр как конструктор и собирать свою собственную базу для обучения. "
            "Для этого воспользуйся инструментами Добавить слово➕ или Удалить слово🔙.\n\nНу что, начнём ⬇️"
        )
        # Отправляем задание
        next_cards_handler(message)

    @bot.message_handler(commands=['cards'])
    def next_cards_handler(message):
        cid = message.chat.id
        word_data = fetch_word(cid)
        if not word_data:
            bot.send_message(cid, "Все слова изучены. Добавьте новые слова, чтобы продолжить.")
            return

        target_word, translate = word_data
        example_usage = get_example_usage(target_word)
        other_words = fetch_random_words(target_word)
        options = [target_word] + other_words
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        # Добавляем кнопки выбора слова
        buttons = [types.KeyboardButton(option) for option in sorted(options)]
        for i in range(0, len(buttons), 2):
            markup.add(*buttons[i:i + 2])  # Добавляем по две кнопки в ряд

        # Добавляем кнопки "Дальше", "Добавить слово", и "Удалить слово"
        markup.add(
            types.KeyboardButton(COMMANDS['NEXT']),
            types.KeyboardButton(COMMANDS['ADD_WORD']),
            types.KeyboardButton(COMMANDS['DELETE_WORD'])
        )

        bot.send_message(
            cid,
            f"Выбери перевод слова:\n🇷🇺 {translate}\nПример использования: {example_usage}",
            reply_markup=markup
        )
        bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['target_word'] = target_word
            data['translate_word'] = translate

    @bot.message_handler(func=lambda message: message.text == COMMANDS['NEXT'])
    def process_next_command(message):
        next_cards_handler(message)

    @bot.message_handler(func=lambda message: message.text == COMMANDS['ADD_WORD'])
    def add_word_handler(message):
        cid = message.chat.id
        user_step[cid] = 1
        bot.send_message(cid, "Введите слово на английском и перевод через запятую.")

    @bot.message_handler(func=lambda message: message.text == COMMANDS['DELETE_WORD'])
    def delete_word_handler(message):
        cid = message.chat.id
        try:
            with connect_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT word_en FROM UserWords WHERE user_id = %s", (cid,))
                user_words = [row[0] for row in cur.fetchall()]

            if not user_words:
                bot.send_message(cid, "Ваш словарь пуст.")
                return

            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
            for word in user_words:
                markup.add(types.KeyboardButton(word))
            bot.send_message(cid, "Выберите слово для удаления:", reply_markup=markup)
            user_step[cid] = 2
        except Exception as e:
            bot.send_message(cid, f"Ошибка при удалении слова: {e}")

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def handle_text_message(message):
        cid = message.chat.id
        text = message.text.strip()
        if user_step.get(cid) == 1:
            try:
                word_en, word_ru = map(str.strip, text.split(','))
                insert_user_word(cid, word_en, word_ru)

                # Получаем обновлённое количество слов
                with connect_db() as conn:
                    cur = conn.cursor()
                    cur.execute("SELECT COUNT(*) FROM UserWords WHERE user_id = %s", (cid,))
                    word_count = cur.fetchone()[0]

                bot.send_message(cid, f"Слово '{word_en}' добавлено! Теперь вы изучаете {word_count} слов.")
                user_step[cid] = 0
                next_cards_handler(message)
            except ValueError:
                bot.send_message(cid, "Введите слово и перевод через запятую, например: cat, кот.")
            except Exception as e:
                bot.send_message(cid, f"Ошибка: {e}")
        elif user_step.get(cid) == 2:
            delete_user_word(cid, text)
            bot.send_message(cid, f"Слово '{text}' удалено из вашего словаря!")
            user_step[cid] = 0
            next_cards_handler(message)
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                target_word = data.get('target_word', '')
                if text.lower() == target_word.lower():
                    bot.send_message(cid, "Отлично! Вы угадали. Нажмите 'Дальше' для продолжения.")
                else:
                    bot.send_message(cid, "Неправильно. Попробуйте ещё раз.")
