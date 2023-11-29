CREATE TABLE IF NOT EXISTS Allbums (
	allbum_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	release_year DATE NOT NULL
);

CREATE TABLE  IF NOT EXISTS Tracks (
	track_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	duration TIME NOT NULL,
	allbum_id INTEGER NOT NULL,
	CONSTRAINT fk_allbum FOREIGN KEY(allbum_id) REFERENCES Allbums(allbum_id)
);

CREATE TABLE IF NOT EXISTS Executors (
	executor_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genres (
	genre_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS GenresExecutors (
	genre_executor_id SERIAL PRIMARY KEY,
	genre_id INTEGER NOT NULL,
	executor_id INTEGER NOT NULL,
	CONSTRAINT fk_genre FOREIGN KEY(genre_id) REFERENCES Genres(genre_id) ON DELETE CASCADE,
	CONSTRAINT fk_executor FOREIGN KEY(executor_id) REFERENCES Executors(executor_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AllbumsExecutors (
	allbums_executor_id SERIAL PRIMARY KEY,
	allbum_id INTEGER NOT NULL,
	executor_id INTEGER NOT NULL,
	CONSTRAINT fk_allbum FOREIGN KEY(allbum_id) REFERENCES Allbums(allbum_id) ON DELETE CASCADE,
	CONSTRAINT fk_executor FOREIGN KEY(executor_id) REFERENCES Executors(executor_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Collections (
	collection_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	release_year DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS CollectionsTracks (
	collection_track_id SERIAL PRIMARY KEY,
	collection_id INTEGER NOT NULL,
	track_id INTEGER NOT NULL,
	CONSTRAINT fk_collection FOREIGN KEY(collection_id) REFERENCES Collections(collection_id) ON DELETE CASCADE,
	CONSTRAINT fk_track FOREIGN KEY(track_id) REFERENCES Tracks(track_id) ON DELETE CASCADE
);