-- EV Charging Slot Booking System
-- Database Schema
-- Run this in pgAdmin > Query Tool


-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Charging stations table
CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    total_slots INT DEFAULT 4,
    charger_type VARCHAR(10) CHECK (charger_type IN ('AC', 'DC')),
    price_per_hour DECIMAL(8,2) DEFAULT 50.00,
    is_active BOOLEAN DEFAULT TRUE
);

-- Bookings table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    station_id INT REFERENCES stations(id),
    slot_date DATE NOT NULL,
    slot_time TIME NOT NULL,
    duration_mins INT DEFAULT 60,
    total_price DECIMAL(8,2),
    status VARCHAR(20) DEFAULT 'confirmed'
        CHECK (status IN ('confirmed', 'cancelled', 'completed')),
    vehicle_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(station_id, slot_date, slot_time)
);

-- Sample data
INSERT INTO stations (name, location, charger_type, price_per_hour) VALUES
('NSUT EV Point A', 'Main Gate, NSUT Dwarka', 'AC', 40.00),
('NSUT EV Point B', 'Hostel Block, NSUT', 'DC', 80.00),
('Dwarka Sec 12 Hub', 'Sector 12, Dwarka Metro', 'AC', 35.00),
('Dwarka Sec 21 Hub', 'Sector 21, Dwarka', 'DC', 75.00);
