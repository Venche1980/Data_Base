-- Таблица жанров
CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Таблица исполнителей
CREATE TABLE artist (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Связующая таблица для исполнителей и жанров (многие ко многим)
CREATE TABLE artist_genre (
    artist_genre_id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES artist(artist_id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genre(genre_id) ON DELETE CASCADE
);

-- Таблица альбомов
CREATE TABLE album (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INTEGER NOT NULL CHECK (release_year >= 1900)
);

-- Связующая таблица для исполнителей и альбомов (многие ко многим)
CREATE TABLE artist_album (
    artist_album_id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES artist(artist_id) ON DELETE CASCADE,
    album_id INTEGER REFERENCES album(album_id) ON DELETE CASCADE
);

-- Таблица треков
CREATE TABLE track (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTEGER NOT NULL CHECK (duration > 0),
    album_id INTEGER REFERENCES album(album_id) ON DELETE CASCADE
);

-- Таблица сборников
CREATE TABLE compilation (
    compilation_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INTEGER NOT NULL CHECK (release_year >= 1900)
);

-- Связующая таблица для треков и сборников (многие ко многим)
CREATE TABLE compilation_track (
    compilation_track_id SERIAL PRIMARY KEY,
    compilation_id INTEGER REFERENCES compilation(compilation_id) ON DELETE CASCADE,
    track_id INTEGER REFERENCES track(track_id) ON DELETE CASCADE
);
