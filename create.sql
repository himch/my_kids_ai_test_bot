-- SQL script to bootstrap the DB:
--
-- Таблица с пользователями бота
CREATE TABLE IF NOT EXISTS users
                (
                tgid INTEGER,
                chatid INTEGER
                );
