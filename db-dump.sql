PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE ip (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	created DATETIME NOT NULL,
	updated DATETIME,
	address TEXT NOT NULL,
	description TEXT,
	device TEXT NOT NULL,
	location TEXT NOT NULL,
	site VARCHAR(11) NOT NULL,
	type TEXT NOT NULL,
	CONSTRAINT site CHECK (site IN ('marie_curie', 'molière'))
);
CREATE TABLE user (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	created DATETIME NOT NULL,
	updated DATETIME,
	generic BOOLEAN DEFAULT (0) NOT NULL,
	disabled BOOLEAN DEFAULT (0) NOT NULL,
	password TEXT NOT NULL,
	role VARCHAR(18) NOT NULL,
	username TEXT NOT NULL,
	CHECK (generic IN (0, 1)),
	CHECK (disabled IN (0, 1)),
	CONSTRAINT role CHECK (role IN ('admin', 'facility_support_1', 'facility_support_2', 'it_support_1', 'it_support_2', 'teacher')),
	UNIQUE (username)
);
INSERT INTO user VALUES(1,'2020-04-08 10:38:54.585129',NULL,0,0,'pbkdf2:sha256:150000$dMRo5KxW$374b67cc274cdf0b30bd367e83d7f3b873c33c9c7dbff415285083d93a6dd0a3','admin','admin');
CREATE TABLE issue (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	created DATETIME NOT NULL,
	updated DATETIME,
	closed DATETIME,
	computer_number TEXT,
	description TEXT,
	location TEXT NOT NULL,
	site VARCHAR(11) NOT NULL,
	status VARCHAR(1) NOT NULL,
	title TEXT NOT NULL,
	type VARCHAR(8) NOT NULL,
	user_id INTEGER,
	username TEXT,
	CONSTRAINT site CHECK (site IN ('marie_curie', 'molière')),
	CONSTRAINT status CHECK (status IN ('1', '2', '3')),
	CONSTRAINT type CHECK (type IN ('facility', 'it')),
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
