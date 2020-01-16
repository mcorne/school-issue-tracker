PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE post (
	created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	updated DATETIME, 
	author_id INTEGER, 
	body TEXT NOT NULL, 
	title TEXT NOT NULL, 
	FOREIGN KEY(author_id) REFERENCES user (id)
);
CREATE TABLE user (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	created DATETIME NOT NULL, 
	updated DATETIME, 
	generic BOOLEAN DEFAULT (0) NOT NULL, 
	disabled BOOLEAN DEFAULT (0) NOT NULL, 
	password TEXT NOT NULL, 
	role VARCHAR(15) NOT NULL, 
	username TEXT NOT NULL, 
	CHECK (generic IN (0, 1)), 
	CHECK (disabled IN (0, 1)), 
	CONSTRAINT role CHECK (role IN ('admin', 'teacher', 'it_technician', 'it_manager', 'service_agent', 'service_manager')), 
	UNIQUE (username)
);
INSERT INTO user VALUES(1,'2020-01-16 11:43:18.726812',NULL,0,0,'pbkdf2:sha256:150000$kmq1GkZH$00b43cf4ba55d2ece52f6f5f1eb0824560862900262aa75befafd5404e6e08d8','admin','admin');
CREATE TABLE issue (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	created DATETIME NOT NULL, 
	updated DATETIME, 
	closed DATETIME, 
	computer_number TEXT, 
	description TEXT, 
	location TEXT NOT NULL, 
	site VARCHAR(11) NOT NULL, 
	title TEXT NOT NULL, 
	type VARCHAR(8) NOT NULL, 
	user_id INTEGER, 
	username TEXT, 
	CONSTRAINT site CHECK (site IN ('marie_curie', 'molière')), 
	CONSTRAINT type CHECK (type IN ('computer', 'other')), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('user',1);
COMMIT;
