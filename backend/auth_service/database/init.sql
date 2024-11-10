CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    email_is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (username, email, hashed_password, is_active, is_admin, email_is_verified)
VALUES
('testuser1', 'testuser1@example.com', 'hashed_password_1', TRUE, FALSE, FALSE);

INSERT INTO users (username, email, hashed_password, is_active, is_admin, email_is_verified)
VALUES
('testuser2', 'testuser2@example.com', 'hashed_password_2', FALSE, TRUE, TRUE);

CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_info VARCHAR(255),
    refresh_token VARCHAR(512) NOT NULL,
    expires_at TIMESTAMP NOT NULL

);
