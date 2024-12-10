CREATE TABLE Users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Words (
    word_id SERIAL PRIMARY KEY,  -- уникальный идентификатор слова
    word_en TEXT NOT NULL,  -- слово на английском
    word_ru TEXT NOT NULL,  -- слово на русском
    category TEXT  -- категория слова (например, цвет, местоимение и т.д.)
);

-- Создание таблицы пользовательских слов
CREATE TABLE UserWords (
    user_word_id SERIAL PRIMARY KEY,  -- уникальный идентификатор пользовательского слова
    user_id BIGINT REFERENCES Users(user_id),  -- идентификатор пользователя, который добавил слово
    word_en TEXT NOT NULL,  -- слово на английском
    word_ru TEXT NOT NULL,  -- слово на русском
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- дата и время добавления слова
);