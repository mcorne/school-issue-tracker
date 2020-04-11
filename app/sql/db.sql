PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE ip (
	id INTEGER NOT NULL, 
	created DATETIME NOT NULL, 
	updated DATETIME, 
	address TEXT NOT NULL, 
	description TEXT, 
	device TEXT NOT NULL, 
	location TEXT NOT NULL, 
	site VARCHAR(100) NOT NULL, 
	type TEXT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (address), 
	CONSTRAINT site CHECK (site IN ('marie_curie', 'molière'))
);
CREATE TABLE user (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	created DATETIME NOT NULL, 
	updated DATETIME, 
	generic BOOLEAN DEFAULT (0) NOT NULL, 
	disabled BOOLEAN DEFAULT (0) NOT NULL, 
	password TEXT NOT NULL, 
	role VARCHAR(100) NOT NULL, 
	username TEXT NOT NULL, 
	CHECK (generic IN (0, 1)), 
	CHECK (disabled IN (0, 1)), 
	CONSTRAINT role CHECK (role IN ('admin', 'facility_support_1', 'facility_support_2', 'it_support_1', 'it_support_2', 'teacher')), 
	UNIQUE (username)
);
INSERT INTO user VALUES(1,'2020-04-11 14:29:52.760563',NULL,0,0,'pbkdf2:sha256:150000$Ahec62sp$0db4dab42073222c958d82a49a7db3f6f297211de8d33bfb5a953a1b82cdb2fd','admin','admin');
CREATE TABLE issue (
	id INTEGER NOT NULL, 
	created DATETIME NOT NULL, 
	updated DATETIME, 
	closed DATETIME, 
	computer_number TEXT, 
	description TEXT, 
	location TEXT NOT NULL, 
	site VARCHAR(100) NOT NULL, 
	status VARCHAR(1) NOT NULL, 
	title TEXT NOT NULL, 
	type VARCHAR(100) NOT NULL, 
	user_id INTEGER NOT NULL, 
	username TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT site CHECK (site IN ('marie_curie', 'molière')), 
	CONSTRAINT status CHECK (status IN ('1', '2', '3')), 
	CONSTRAINT type CHECK (type IN ('it', 'facility')), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE message (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	created DATETIME NOT NULL, 
	updated DATETIME, 
	content TEXT, 
	issue_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	username TEXT, 
	FOREIGN KEY(issue_id) REFERENCES issue (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('user',1);
CREATE INDEX ip_default_sort ON ip (site, location, type, device);
CREATE INDEX issue_default_sort ON issue (type, status, updated, created);
CREATE INDEX issue_user_id ON issue (user_id);
CREATE INDEX message_user_id ON message (user_id);
CREATE INDEX message_issue_id ON message (issue_id);
COMMIT;
