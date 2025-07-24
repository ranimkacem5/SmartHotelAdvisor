-- Création des tables pour SmartHotelAdvisor

-- Utilisateurs (clients, personnel, admins)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('client', 'personnel', 'admin')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chambres de l’hôtel
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    number VARCHAR(10) UNIQUE NOT NULL,
    type VARCHAR(50), -- ex: simple, double, suite
    capacity INT,
    price_per_night DECIMAL(10, 2),
    amenities TEXT, -- équipements: wifi, TV, etc.
    is_available BOOLEAN DEFAULT TRUE
);

-- Réservations
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    room_id INT REFERENCES rooms(id) ON DELETE CASCADE,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_price DECIMAL(10, 2),
    payment_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Réclamations
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'en attente', -- ou 'traitée'
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exemple de données de test
INSERT INTO users (username, password, role) VALUES
('admin', 'adminpass', 'admin'),
('client1', 'clientpass', 'client');

INSERT INTO rooms (number, type, capacity, price_per_night, amenities)
VALUES 
('101', 'double', 2, 150.00, 'wifi, tv, balcon'),
('102', 'simple', 1, 90.00, 'wifi');

