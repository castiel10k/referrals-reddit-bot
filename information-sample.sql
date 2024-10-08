BEGIN TRANSACTION;

DROP TABLE IF EXISTS "linkTitleBody";
DROP TABLE IF EXISTS "referralTitle";
CREATE TABLE IF NOT EXISTS "referralTitle" (
	"id"	INTEGER NOT NULL UNIQUE,
	"title"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "referralBody";
CREATE TABLE IF NOT EXISTS "referralBody" (
	"id"	INTEGER NOT NULL UNIQUE,
	"body"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "linkTitleBody" (
	"idTitle"	INTEGER NOT NULL UNIQUE,
	"idBody"	INTEGER NOT NULL UNIQUE,
	FOREIGN KEY("idTitle") REFERENCES "referralTitle"("id"),
	FOREIGN KEY("idBody") REFERENCES "referralBody"("id")
);
INSERT INTO "referralTitle" ("id","title") VALUES (1,'Title');
INSERT INTO "referralBody" ("id","body") VALUES (1,'Body');
INSERT INTO "linkTitleBody" ("idTitle","idBody") VALUES (1,1);
COMMIT;
