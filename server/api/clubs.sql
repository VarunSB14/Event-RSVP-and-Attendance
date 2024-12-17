DROP TABLE IF EXISTS clubs CASCADE;

CREATE TABLE clubs (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    capacity INTEGER NOT NULL,
    yellow_threshold INTEGER NOT NULL,
    current_occupancy INTEGER DEFAULT 0,
    music VARCHAR(100)
);

INSERT INTO clubs (name, location, capacity, yellow_threshold, current_occupancy, music) VALUES
('Club Arcane', 'New York', 100, 70, 0, 'Rock'),
('Studio 52', 'New York', 52, 32, 0, 'Rock'),
('Club Underground', 'Los Angeles', 50, 30, 0, 'Pop'),
('Club Soda', 'Chicago', 20, 12, 0, 'Synth');

SELECT * FROM clubs;