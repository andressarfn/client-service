CREATE DATABASE client_service_db;

\c client_service_db;
CREATE SCHEMA IF NOT EXISTS favorites;
CREATE USER client_service_user WITH PASSWORD 'client_service_password';


CREATE TABLE IF NOT EXISTS favorites.clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS favorites.favorites (
    id SERIAL PRIMARY KEY,
    client_id INT REFERENCES favorites.clients(id) ON DELETE CASCADE,
    product_id INT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_client_product ON favorites.favorites (client_id, product_id);

GRANT USAGE ON SCHEMA favorites TO client_service_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA favorites TO client_service_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA favorites TO client_service_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA favorites TO client_service_user;

-- SCRIPTS TO TEST

INSERT INTO favorites.clients (name, email) VALUES ('John Doe', 'john@example.com');
INSERT INTO favorites.favorites (client_id, product_id) VALUES (1, 1);
