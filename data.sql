-- Вставка данных в таблицу жанров
INSERT INTO genre (name) VALUES ('Рок');
INSERT INTO genre (name) VALUES ('Поп');
INSERT INTO genre (name) VALUES ('Джаз');
INSERT INTO genre (name) VALUES ('Электронная музыка');
INSERT INTO genre (name) VALUES ('Шансон');

-- Вставка данных в таблицу исполнителей
INSERT INTO artist (name) VALUES ('Кино');
INSERT INTO artist (name) VALUES ('Алла Пугачёва');
INSERT INTO artist (name) VALUES ('Игорь Бутман');
INSERT INTO artist (name) VALUES ('ДДТ');
INSERT INTO artist (name) VALUES ('Земфира');
INSERT INTO artist (name) VALUES ('Мумий Тролль');

-- Вставка данных в таблицу альбомов
INSERT INTO album (title, release_year) VALUES ('Звезда по имени Солнце', 1989);
INSERT INTO album (title, release_year) VALUES ('Арлекино', 1976);
INSERT INTO album (title, release_year) VALUES ('Квартет', 2000);
INSERT INTO album (title, release_year) VALUES ('Иначе', 2013);
INSERT INTO album (title, release_year) VALUES ('Морская', 1997);
INSERT INTO album (title, release_year) VALUES ('Энергия', 1991);

-- Вставка данных в таблицу треков
INSERT INTO track (title, duration, album_id) VALUES ('Звезда по имени Солнце', 280, 1);
INSERT INTO track (title, duration, album_id) VALUES ('Арлекино', 240, 2);
INSERT INTO track (title, duration, album_id) VALUES ('Миллион алых роз', 300, 2);
INSERT INTO track (title, duration, album_id) VALUES ('Квартет', 600, 3);
INSERT INTO track (title, duration, album_id) VALUES ('Свободный полёт', 420, 3);
INSERT INTO track (title, duration, album_id) VALUES ('Группа крови', 290, 1);
INSERT INTO track (title, duration, album_id) VALUES ('Мы ждём перемен', 320, 1);
INSERT INTO track (title, duration, album_id) VALUES ('Иначе', 350, 4);
INSERT INTO track (title, duration, album_id) VALUES ('Уходи', 270, 5);
INSERT INTO track (title, duration, album_id) VALUES ('Энергия', 310, 6);
INSERT INTO track (title, duration, album_id) VALUES ('Гуляй, Вася!', 275, 6);

-- Вставка данных в таблицу сборников
INSERT INTO compilation (title, release_year) VALUES ('Лучшие рок-хиты', 1995);
INSERT INTO compilation (title, release_year) VALUES ('Золотая коллекция поп-музыки', 2005);
INSERT INTO compilation (title, release_year) VALUES ('Джазовые импровизации', 2010);
INSERT INTO compilation (title, release_year) VALUES ('Легендарные треки', 2015);
INSERT INTO compilation (title, release_year) VALUES ('Русский рок на все времена', 2018);
INSERT INTO compilation (title, release_year) VALUES ('Популярные треки 90-х', 2020);
INSERT INTO compilation (title, release_year) VALUES ('Лучшие хиты 2000-х', 2021);

-- Вставка данных в таблицу artist_genre (связь исполнителей с жанрами)
INSERT INTO artist_genre (artist_id, genre_id) VALUES (1, 1);
INSERT INTO artist_genre (artist_id, genre_id) VALUES (2, 2);
INSERT INTO artist_genre (artist_id, genre_id) VALUES (3, 3);
INSERT INTO artist_genre (artist_id, genre_id) VALUES (4, 1);
INSERT INTO artist_genre (artist_id, genre_id) VALUES (4, 2);
INSERT INTO artist_genre (artist_id, genre_id) VALUES (5, 1);
INSERT INTO artist_genre (artist_id, genre_id) VALUES (6, 4);
INSERT INTO artist_genre (artist_id, genre_id) VALUES (6, 5);

-- Вставка данных в таблицу artist_album (связь исполнителей с альбомами)
INSERT INTO artist_album (artist_id, album_id) VALUES (1, 1);
INSERT INTO artist_album (artist_id, album_id) VALUES (2, 2);
INSERT INTO artist_album (artist_id, album_id) VALUES (3, 3);
INSERT INTO artist_album (artist_id, album_id) VALUES (4, 1);
INSERT INTO artist_album (artist_id, album_id) VALUES (5, 4);
INSERT INTO artist_album (artist_id, album_id) VALUES (6, 5);
INSERT INTO artist_album (artist_id, album_id) VALUES (6, 6);

-- Вставка данных в таблицу compilation_track (связь треков с сборниками)
INSERT INTO compilation_track (compilation_id, track_id) VALUES (1, 1);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (1, 6);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (2, 2);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (2, 3);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (3, 4);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (3, 5);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (4, 1);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (4, 2);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (4, 4);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (5, 7);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (5, 8);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (6, 9);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (6, 3);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (7, 10);
INSERT INTO compilation_track (compilation_id, track_id) VALUES (7, 11);