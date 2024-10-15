CREATE TABLE users (
    userid SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    work_time INTERVAL NOT NULL,
    no_work_time INTERVAL NOT NULL,
    end_time TIMESTAMP NOT NULL
);

-- Вставляем тестовые данные
INSERT INTO users (username, start_time, work_time, no_work_time, end_time) VALUES
('Андрей гей52', '2024-10-01 09:00:00', '52:00:00', '01:00:00', '2024-10-01 11:00:00');
CREATE TABLE users2 (
    userid SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    work_time INTERVAL NOT NULL,
    no_work_time INTERVAL NOT NULL,
    end_time TIMESTAMP NOT NULL
);
