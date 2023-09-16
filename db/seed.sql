BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	CHAR(32) NOT NULL,
	"name"	VARCHAR NOT NULL,
	"surname"	VARCHAR NOT NULL,
	"email"	VARCHAR NOT NULL,
	"phone"	VARCHAR NOT NULL,
	"created_at"	VARCHAR NOT NULL,
	"updated_at"	VARCHAR,
	"deleted_at"	VARCHAR,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "badge_readers" (
	"id"	CHAR(32) NOT NULL,
	"ip_address"	VARCHAR NOT NULL,
	"location"	VARCHAR NOT NULL,
	"created_at"	VARCHAR NOT NULL,
	"updated_at"	VARCHAR,
	"deleted_at"	VARCHAR,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "badges" (
	"id"	CHAR(32) NOT NULL,
	"code"	INTEGER NOT NULL,
	"created_at"	VARCHAR NOT NULL,
	"updated_at"	VARCHAR,
	"deleted_at"	VARCHAR,
	"user_id"	CHAR(32) NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "badge_readers_badges" (
	"badge_reader_id"	CHAR(32) NOT NULL,
	"badge_id"	CHAR(32) NOT NULL,
	FOREIGN KEY("badge_id") REFERENCES "badges"("id"),
	FOREIGN KEY("badge_reader_id") REFERENCES "badge_readers"("id"),
	PRIMARY KEY("badge_reader_id","badge_id")
);
CREATE TABLE IF NOT EXISTS "accesses" (
	"id"	CHAR(32) NOT NULL,
	"in_timestamp"	VARCHAR,
	"out_timestamp"	VARCHAR,
	"badge_id"	CHAR(32) NOT NULL,
	"badge_reader_id"	CHAR(32) NOT NULL,
	FOREIGN KEY("badge_reader_id") REFERENCES "badge_readers"("id"),
	FOREIGN KEY("badge_id") REFERENCES "badges"("id"),
	PRIMARY KEY("id")
);
INSERT INTO "users" ("id","name","surname","email","phone","created_at","updated_at","deleted_at") VALUES ('539b82d462ea494bb0a4f8888442df5e','Mario','Rossi','mario.rossi@somedomain.com','+391234567890','2023-09-16 12:10:40+0200',NULL,NULL),
 ('fde0bc87558d4e8282a92685c4c80058','Giovanni','Verdi','giovanni.verdi@somedomain.com','+390000000000','2023-09-16 12:10:40+0200',NULL,NULL),
 ('7ccc293158f8481d84cb8c4247a62c3c','Francesco','Di Muro','dimurofrancesco@virgilio.it','+393801234567','2023-09-16 12:10:40+0200',NULL,NULL);
INSERT INTO "badge_readers" ("id","ip_address","location","created_at","updated_at","deleted_at") VALUES ('60e9dd146b424b9c9f2813323b5ac97c','192.168.150.10','Ingresso principale','2023-09-16 12:10:40+0200',NULL,NULL),
 ('847d73a35128425b8f6ccf124b7eea72','192.168.150.11','Officina','2023-09-16 12:10:40+0200',NULL,NULL),
 ('bae49e5a8f0140778e9a51dcaed09001','192.168.150.12','Manifattura','2023-09-16 12:10:40+0200',NULL,NULL);
INSERT INTO "badges" ("id","code","created_at","updated_at","deleted_at","user_id") VALUES ('a0bbc41e122546ffa4f6eb1592e68930',1234,'2023-09-16 12:10:40+0200',NULL,NULL,'539b82d462ea494bb0a4f8888442df5e'),
 ('c9a34e3f488249419b97e427200e8317',5678,'2023-09-16 12:10:40+0200',NULL,NULL,'7ccc293158f8481d84cb8c4247a62c3c'),
 ('3cf1841df36148439dcf78008ddf18dc',9012,'2023-09-16 12:10:40+0200',NULL,NULL,'fde0bc87558d4e8282a92685c4c80058');
INSERT INTO "badge_readers_badges" ("badge_reader_id","badge_id") VALUES ('60e9dd146b424b9c9f2813323b5ac97c','a0bbc41e122546ffa4f6eb1592e68930'),
 ('847d73a35128425b8f6ccf124b7eea72','a0bbc41e122546ffa4f6eb1592e68930'),
 ('60e9dd146b424b9c9f2813323b5ac97c','c9a34e3f488249419b97e427200e8317'),
 ('847d73a35128425b8f6ccf124b7eea72','c9a34e3f488249419b97e427200e8317'),
 ('bae49e5a8f0140778e9a51dcaed09001','c9a34e3f488249419b97e427200e8317'),
 ('60e9dd146b424b9c9f2813323b5ac97c','3cf1841df36148439dcf78008ddf18dc'),
 ('847d73a35128425b8f6ccf124b7eea72','3cf1841df36148439dcf78008ddf18dc');
COMMIT;
