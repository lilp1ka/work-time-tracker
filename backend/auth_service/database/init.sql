CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,                 -- Уникальный идентификатор сессии
    user_id INT NOT NULL,                  -- Идентификатор пользователя (можно использовать как id из другого микросервиса)
    device_info VARCHAR(255),              -- Информация о устройстве (например, название, версия и т.д.)
    refresh_token VARCHAR(512) NOT NULL,   -- JWT refresh токен
    issued_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Время, когда токен был выдан
    expires_at TIMESTAMP NOT NULL,         -- Время, когда токен истекает
    valid BOOLEAN DEFAULT TRUE              -- Флаг, указывающий на то, валиден ли токен
);
