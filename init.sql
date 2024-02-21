CREATE DATABASE IF NOT EXISTS spider;
USE spider;

CREATE TABLE IF NOT EXISTS page (
	id VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	url VARCHAR(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	file_location VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
	crawl_attempts INT(32) DEFAULT 0 NOT NULL,
	discover_timestamp datetime DEFAULT CURRENT_TIMESTAMP  NOT NULL,
	crawl_timestamp datetime NULL,
	CONSTRAINT `PRIMARY` PRIMARY KEY (id)
);

SET @x := (SELECT COUNT(*) FROM information_schema.statistics WHERE table_name = 'page' AND index_name = 'idx_url' AND table_schema = database());
SET @sql := if(@x > 0, 'SELECT ''Index exists.''', 'CREATE UNIQUE INDEX idx_url ON page(url);');
PREPARE stmt FROM @sql;
EXECUTE stmt;
