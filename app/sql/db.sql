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
	site VARCHAR(11) NOT NULL, 
	type TEXT NOT NULL, 
	PRIMARY KEY (id), 
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
INSERT INTO user VALUES(1,'2020-04-11 13:25:07.763318',NULL,0,0,'pbkdf2:sha256:150000$yVBgiOiZ$03440b2d37b3bc7b06933a9f9ba779d67071ec45c002fa99ca93e42861dae50d','admin','admin');
CREATE TABLE issue (
	id INTEGER NOT NULL, 
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
	issue_id INTEGER, 
	user_id INTEGER, 
	username TEXT, 
	FOREIGN KEY(issue_id) REFERENCES issue (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('user',1);
CREATE INDEX ip_default_sort ON ip (site, location, type, device);
CREATE INDEX issue_default_sort ON issue (type, status, updated, created);
COMMIT;
