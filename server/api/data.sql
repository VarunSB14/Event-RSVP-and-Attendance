DROP TABLE IF EXISTS rsvps CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL
);

-- Create events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    time TIME NOT NULL,
    location VARCHAR(200) NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0),
    available_spots INT NOT NULL CHECK (available_spots >= 0)
);

-- Create rsvps table
CREATE TABLE rsvps (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    event_id INT REFERENCES events(id) ON DELETE CASCADE,
    status VARCHAR(20) CHECK (status IN ('RSVP', 'Attended'))
);

-- Seed initial data for users
INSERT INTO users (name, email, password) VALUES
('John Doe', 'john.doe@example.com', 'bed4efa1d4fdbd954bd3705d6a2a78270ec9a52ecfbfb010c61862af5c76af1761ffeb1aef6aca1bf5d02b3781aa854fabd2b69c790de74e17ecfec3cb6ac4bf'), -- password123
('Jane Smith', 'jane.smith@example.com', '5acf6014ded240600f62f15259d4107520e91472dafbbf85e9f90dac74f1fc6d7567cf489802ec09d2de2ffdc20a40612dfd063b511c83f98832811e9af2f090'); -- password124

-- Seed initial data for events
INSERT INTO events (title, description, date, time, location, capacity, available_spots) VALUES
('Tech Conference 2024', 'A conference for tech enthusiasts.', '2024-01-15', '10:00', 'Convention Center', 100, 100),
('Art Workshop', 'Learn painting techniques.', '2024-01-20', '14:00', 'Art Studio', 20, 20),
('Music Concert', 'Live performance by famous bands.', '2024-02-10', '18:00', 'Music Hall', 500, 500);

ALTER TABLE events ADD COLUMN category VARCHAR(50);
