--
-- File generated with SQLiteStudio v3.4.3 on 周三 8月 16 15:39:38 2023
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: user
DROP TABLE IF EXISTS user;
CREATE TABLE IF NOT EXISTS "user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "nickname" varchar(64) NOT NULL);
INSERT INTO user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, nickname) VALUES (1, 'pbkdf2_sha256$216000$AZ2u7Eg75x9z$dRO88eFBUnWt+VcZXYnXcD3/4ftgE/9z5PMusU3MxHU=', NULL, 0, 'admin', '', '', '', 1, 1, '2023-05-31 01:06:15.151877', '管理员');

-- Index: sqlite_autoindex_user_1
DROP INDEX IF EXISTS sqlite_autoindex_user_1;
CREATE UNIQUE INDEX IF NOT EXISTS sqlite_autoindex_user_1 ON user (username COLLATE BINARY);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
