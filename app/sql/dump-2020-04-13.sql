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
INSERT INTO "ip" VALUES(1,'2020-04-12 19:36:49.623258',NULL,'1.1.1.1',NULL,'hp','100','marie_curie','serveur');
INSERT INTO "ip" VALUES(2,'2020-04-12 19:37:33.874050','2020-04-12 19:37:58.148682','1.1.1.2','couleur','hp','200','molière','imprimante');
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
INSERT INTO "user" VALUES(1,'2020-04-12 17:00:45.661073',NULL,0,0,'pbkdf2:sha256:150000$eUAz4y6p$3b53c9be64a353317fd77e5bc9be4802217bfccddec4a5ee9f76ff64bebcc5cb','admin','admin');
INSERT INTO "user" VALUES(2,'2020-04-12 19:33:51.962081',NULL,0,0,'pbkdf2:sha256:150000$JW0feEBY$21d8ccd8efcd8da6bc2867e0963ee123990fbf219b7086ae04b3ef9b0bc6a136','facility_support_1','eric');
INSERT INTO "user" VALUES(3,'2020-04-12 19:34:28.081332',NULL,0,0,'pbkdf2:sha256:150000$DeLM2kYI$33316b269b803162467228a4619ca73422c61a1a72b02c56e65237fec2a1ef7b','it_support_2','samuel');
INSERT INTO "user" VALUES(4,'2020-04-12 19:35:11.336650',NULL,1,0,'pbkdf2:sha256:150000$m2QmLJIB$4b1232392371b76856f90cee1d2280fa129e5a02157eceb38c8ac3f1013c4be3','teacher','prof');
INSERT INTO "user" VALUES(5,'2020-04-12 19:52:17.666193',NULL,0,0,'pbkdf2:sha256:150000$s7v42l0h$5e8ae2d06b7398df47117967e89620b24b444d6a1bbd663db9d888e071418bb1','facility_support_2','georges');
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
INSERT INTO "issue" VALUES(1,'2020-04-12 19:40:21.648229','2020-04-12 19:43:37.701637',NULL,'100','ne marche plus','111','marie_curie','2','pc hs','it',4,'Gérard Landru');
INSERT INTO "issue" VALUES(2,'2020-04-12 19:42:23.524413','2020-04-12 19:52:58.154686','2020-04-12 19:52:58.154673',NULL,'papiers par terre partout','couloir RC','molière','3','couloir sale','facility',4,'Jeanne Dumond');
INSERT INTO "issue" VALUES(3,'2020-04-12 19:47:12.933284','2020-04-12 20:01:38.510273',NULL,NULL,'il y a eu un flash dans l''interrupteur','200','marie_curie','2','pas de lumière','facility',4,'Gérard Landru');
INSERT INTO "issue" VALUES(4,'2020-04-12 19:49:22.605682',NULL,NULL,NULL,'imprimante vers la fenêtre','111','marie_curie','1','ça n''imprime plus en vert','it',4,'Jeanne Dumond');
INSERT INTO "issue" VALUES(5,'2020-04-12 19:56:06.258307','2020-04-12 19:57:45.514481',NULL,NULL,'débris de vitre par terre','batiment A','molière','1','porte d''entrée cassée','facility',4,'Albertine Allo');
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
INSERT INTO "message" VALUES(1,'2020-04-12 19:43:37.695536',NULL,'faut changer l''alim',1,3,NULL);
INSERT INTO "message" VALUES(2,'2020-04-12 19:50:55.596546',NULL,'c''est ramassé',2,2,NULL);
INSERT INTO "message" VALUES(3,'2020-04-12 19:52:58.158544',NULL,'Clôture de la demande',2,5,NULL);
INSERT INTO "message" VALUES(4,'2020-04-12 19:56:53.042694',NULL,'elle ne ferme plus',5,4,'Albertine Allo');
INSERT INTO "message" VALUES(5,'2020-04-12 19:57:45.518975',NULL,'Requalifié en demande pour les services généraux',5,3,NULL);
INSERT INTO "message" VALUES(6,'2020-04-12 20:01:38.502675',NULL,'on a commandé un nouvel interrupteur',3,5,NULL);
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('user',5);
INSERT INTO "sqlite_sequence" VALUES('message',6);
CREATE INDEX ip_default_sort ON ip (site, location, type, device);
CREATE INDEX issue_user_id ON issue (user_id);
CREATE INDEX issue_default_sort ON issue (type, status, updated, created);
CREATE INDEX message_user_id ON message (user_id);
CREATE INDEX message_issue_id ON message (issue_id);
COMMIT;
