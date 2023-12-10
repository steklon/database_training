CREATE TABLE IF NOT EXISTS allbums (
    allbum_id    SERIAL
    PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    release_year INTEGER      NOT NULL
                 CHECK(release_year >= 1930)
);

CREATE TABLE IF NOT EXISTS tracks (
    track_id     SERIAL
    PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    duration     INTEGER      NOT NULL
	         CHECK(duration <= 1800),
    allbum_id    INTEGER      NOT NULL,
	         CONSTRAINT fk_allbum
    FOREIGN KEY(allbum_id)
	         REFERENCES allbums(allbum_id)
);

CREATE TABLE IF NOT EXISTS executors (
    executor_id  SERIAL
    PRIMARY KEY,
    name         VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id     SERIAL
    PRIMARY KEY,
    name         VARCHAR(100) NOT NULL
	         UNIQUE
);

CREATE TABLE IF NOT EXISTS genres_executors (
    genre_executor_id SERIAL
    PRIMARY KEY,
    genre_id          INTEGER NOT NULL,
    executor_id       INTEGER NOT NULL,
                      CONSTRAINT fk_genre
    FOREIGN KEY(genre_id)
                      REFERENCES genres(genre_id)       ON DELETE CASCADE,
                      CONSTRAINT fk_executor
    FOREIGN KEY(executor_id)
                      REFERENCES executors(executor_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS allbums_executors (
    allbums_executor_id SERIAL
    PRIMARY KEY,
    allbum_id           INTEGER NOT NULL,
    executor_id         INTEGER NOT NULL,
	                CONSTRAINT fk_allbum
    FOREIGN KEY(allbum_id)
	                REFERENCES allbums(allbum_id)     ON DELETE CASCADE,
	                CONSTRAINT fk_executor
    FOREIGN KEY(executor_id)
	                REFERENCES executors(executor_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS collections (
    collection_id SERIAL
    PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    release_year  INTEGER      NOT NULL
	          CHECK(release_year >= 1931)
);

CREATE TABLE IF NOT EXISTS collections_tracks (
    collection_track_id SERIAL
    PRIMARY KEY,
    collection_id       INTEGER NOT NULL,
    track_id            INTEGER NOT NULL,
	                CONSTRAINT fk_collection
    FOREIGN KEY(collection_id)
	                REFERENCES collections(collection_id) ON DELETE CASCADE,
	                CONSTRAINT fk_track
    FOREIGN KEY(track_id)
	                REFERENCES tracks(track_id)           ON DELETE CASCADE
);
