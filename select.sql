-- Название и продолжительность самого длительного трека
SELECT name, duration
  FROM tracks
 WHERE duration = (
       SELECT MAX(duration)
         FROM tracks);

-- Название треков, продолжительность которых не менее 3,5 минут
SELECT name
  FROM tracks
 WHERE duration >= 240;

-- Названия сборников, вышедших в период с 2018 по 2020 год включительно
SELECT name
  FROM collections
 WHERE (release_year >= 2018)
   AND (release_year <= 2020);

-- Исполнители, чьё имя состоит из одного слова
SELECT name FROM executors
 WHERE NOT name LIKE '% %';

-- Название треков, которые содержат слово «мой» или «my»
SELECT name FROM tracks
 WHERE name LIKE '%my%'
    OR name LIKE '%мой%';

-- Количество исполнителей в каждом жанре
SELECT g.name, COUNT(e.executor_id)
  FROM genres_executors e
  JOIN genres g
    ON g.genre_id = e.genre_id
 GROUP BY g.genre_id;

-- Количество треков, вошедших в альбомы 2019–2020 годов
SELECT a.name, COUNT(t.track_id), a.release_year
  FROM tracks t
  JOIN allbums a
    ON a.allbum_id = t.allbum_id
 WHERE (release_year >= 2019)
   AND (release_year <= 2020)
 GROUP BY a.allbum_id;

-- Средняя продолжительность треков по каждому альбому
SELECT a.name, AVG(t.duration)
  FROM tracks t
  JOIN allbums a
    ON a.allbum_id = t.allbum_id
 GROUP BY a.allbum_id;

-- Все исполнители, которые не выпустили альбомы в 2020 году
SELECT e.name, a.name, a.release_year
  FROM allbums_executors ae
  JOIN executors e
    ON e.executor_id = ae.executor_id
  JOIN allbums a
    ON a.allbum_id = ae.allbum_id
 WHERE NOT release_year = 2020;

-- Названия сборников, в которых присутствует исполнитель Kurt Cobain
SELECT DISTINCT c.name, e.name
  FROM collections_tracks ct
  JOIN collections c
    ON ct.collection_id = c.collection_id
  JOIN tracks t
    ON ct.track_id = t.track_id
  JOIN allbums a
    ON t.allbum_id = a.allbum_id
  JOIN allbums_executors ae
    ON ae.allbum_id = a.allbum_id
  JOIN executors e
    ON ae.executor_id = e.executor_id
 WHERE e.name = 'Kurt Cobain';

-- Названия альбомов, в которых присутствуют исполнители более чем одного жанра
SELECT DISTINCT a.name
  FROM allbums_executors ae
  JOIN allbums a
    ON ae.allbum_id = a.allbum_id
  JOIN executors e
    ON ae.executor_id = e.executor_id
  JOIN genres_executors ge
    ON ge.executor_id = e.executor_id
  JOIN genres g
    ON ge.genre_id = g.genre_id
 GROUP BY a.allbum_id, e.executor_id
HAVING COUNT(ge.genre_id) > 1;

-- Наименования треков, которые не входят в сборники
SELECT t.name
  FROM tracks t
  LEFT JOIN collections_tracks ct
    ON t.track_id = ct.track_id
 WHERE ct.track_id IS NULL;

-- Исполнитель или исполнители, написавшие самый короткий по продолжительности трек
SELECT e.name, t.duration, t.name
  FROM executors e
  JOIN allbums_executors ae
    ON ae.executor_id = e.executor_id
  JOIN allbums a
    ON ae.allbum_id = a.allbum_id
  JOIN tracks t
    ON t.allbum_id = a.allbum_id
 GROUP BY e.name, t.duration, t.name
HAVING t.duration = (
       SELECT MIN(duration)
         FROM tracks);

-- Названия альбомов, содержащих наименьшее количество треков
SELECT DISTINCT a.name
  FROM allbums a
  LEFT JOIN tracks t
    ON t.allbum_id = a.allbum_id
 WHERE t.allbum_id IN
       (SELECT allbum_id
          FROM tracks
         GROUP BY allbum_id
        HAVING COUNT(allbum_id) = (
               SELECT COUNT(allbum_id)
                 FROM tracks
                GROUP BY allbum_id
                ORDER BY count(allbum_id)
                LIMIT 1))
 ORDER BY a.name;