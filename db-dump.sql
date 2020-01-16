PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
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
INSERT INTO user VALUES(1,'2020-01-16 16:38:05.411108',NULL,0,0,'pbkdf2:sha256:150000$AEaD3G6n$a470b61c76216e7a291b03f9ced4a4c416eda3872fd470c8a7a65f9ed05a581c','admin','admin');
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
CREATE TABLE message (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	created DATETIME NOT NULL, 
	updated DATETIME, 
	content TEXT, 
	issue_id INTEGER, 
	user_id INTEGER, 
	username TEXT, 
	FOREIGN KEY(issue_id) REFERENCES issue (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('user',1);
COMMIT;
