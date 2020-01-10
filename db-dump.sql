PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
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
CREATE TABLE post (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated DATETIME, 
	author_id INTEGER, 
	body TEXT NOT NULL, 
	title TEXT NOT NULL, 
	FOREIGN KEY(author_id) REFERENCES user (id)
);
DELETE FROM sqlite_sequence;
COMMIT;
