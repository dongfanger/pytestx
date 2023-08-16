--
-- File generated with SQLiteStudio v3.4.3 on 周三 8月 16 15:39:24 2023
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: project
DROP TABLE IF EXISTS project;
CREATE TABLE IF NOT EXISTS "project" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "name" varchar(100) NOT NULL UNIQUE, "git_repository" varchar(100) NULL, "git_branch" varchar(100) NULL, "last_sync_time" datetime NULL);
INSERT INTO project (id, created_at, updated_at, name, git_repository, git_branch, last_sync_time) VALUES (1, '2023-06-27 08:49:49.355886', '2023-07-20 08:32:08.757259', '默认项目', 'https://gitee.com/dongfanger/tep-project.git', 'master', '2023-07-20 08:32:08');

-- Index: sqlite_autoindex_project_1
DROP INDEX IF EXISTS sqlite_autoindex_project_1;
CREATE UNIQUE INDEX IF NOT EXISTS sqlite_autoindex_project_1 ON project (name COLLATE BINARY);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
