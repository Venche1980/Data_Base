-- Задание 2
-- Название и продолжительность самого длительного трека
SELECT title, duration FROM track ORDER BY duration DESC LIMIT 1;

-- Название треков, продолжительность которых не менее 3,5 минут
SELECT title FROM track WHERE duration >= 210;

-- Названия сборников, вышедших в период с 2018 по 2020 год включительно
SELECT title FROM compilation WHERE release_year BETWEEN 2018 AND 2020;

-- Исполнители, чьё имя состоит из одного слова
SELECT name FROM artist WHERE name NOT LIKE '% %';

-- Название треков, которые содержат слово "мой" или "my"
SELECT title FROM track WHERE title ILIKE '%мой%' OR title ILIKE '%my%';

-- Задание 3
-- Количество исполнителей в каждом жанре
SELECT genre.name, COUNT(artist_genre.artist_id)
FROM genre
LEFT JOIN artist_genre ON genre.genre_id = artist_genre.genre_id
GROUP BY genre.name;

-- Количество треков, вошедших в альбомы 2019–2020 годов
SELECT COUNT(track.track_id)
FROM track
JOIN album ON track.album_id = album.album_id
WHERE album.release_year BETWEEN 2019 AND 2020;

-- Средняя продолжительность треков по каждому альбому
SELECT album.title, AVG(track.duration)
FROM album
JOIN track ON album.album_id = track.album_id
GROUP BY album.title;

-- Все исполнители, которые не выпустили альбомы в 2020 году
SELECT artist.name
FROM artist
WHERE artist.artist_id NOT IN (
    SELECT artist_album.artist_id
    FROM artist_album
    JOIN album ON artist_album.album_id = album.album_id
    WHERE album.release_year = 2020
);

-- Названия сборников, в которых присутствует конкретный исполнитель (например, "Кино")
SELECT compilation.title
FROM compilation
JOIN compilation_track ON compilation.compilation_id = compilation_track.compilation_id
JOIN track ON compilation_track.track_id = track.track_id
JOIN album ON track.album_id = album.album_id
JOIN artist_album ON album.album_id = artist_album.album_id
JOIN artist ON artist_album.artist_id = artist.artist_id
WHERE artist.name = 'Кино';
