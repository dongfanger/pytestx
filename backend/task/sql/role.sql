--
-- File generated with SQLiteStudio v3.4.3 on 周三 8月 16 15:38:48 2023
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: role
DROP TABLE IF EXISTS role;
CREATE TABLE IF NOT EXISTS "role" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(64) NOT NULL);
INSERT INTO role (id, created_at, updated_at, name) VALUES (1, '2010-07-01 10:20:30', '2010-07-01 10:20:30', '管理员');
INSERT INTO role (id, created_at, updated_at, name) VALUES (2, '2010-07-01 10:20:30', '2010-07-01 10:20:30', '测试');
INSERT INTO role (id, created_at, updated_at, name) VALUES (3, '2010-07-01 10:20:30', '2010-07-01 10:20:30', '开发');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
