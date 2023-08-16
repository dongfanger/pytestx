--
-- File generated with SQLiteStudio v3.4.3 on 周三 8月 16 15:39:51 2023
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: user_role
DROP TABLE IF EXISTS user_role;
CREATE TABLE IF NOT EXISTS "user_role" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" integer NOT NULL, "role_id" integer NOT NULL);
INSERT INTO user_role (id, created_at, updated_at, user_id, role_id) VALUES (1, '2010-07-01 10:20:30', '2010-07-01 10:20:30', 1, 1);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
