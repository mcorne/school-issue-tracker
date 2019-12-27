PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username TEXT NOT NULL, 
	password TEXT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (password)
);
CREATE TABLE post (
	id INTEGER NOT NULL, 
	author_id INTEGER, 
	created DATETIME NOT NULL, 
	title TEXT NOT NULL, 
	body TEXT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES user (id)
);
DELETE FROM sqlite_sequence;
COMMIT;
