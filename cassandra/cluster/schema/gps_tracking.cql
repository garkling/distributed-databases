-- most important data
CREATE KEYSPACE IF NOT EXISTS gps_tracking
    WITH REPLICATION = {
        'class': 'SimpleStrategy',
        'replication_factor': 3
        };

USE gps_tracking;

CREATE TABLE IF NOT EXISTS positions
(
    device_id UUID,
    date      DATE,
    timestamp BIGINT,
    latitude  DECIMAL,
    longitude DECIMAL,
    speed     DECIMAL,
    PRIMARY KEY ((device_id, date), timestamp)
);

INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 1714206413709, 40.7677, 24.0141, 26.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 1714206414309, 40.7677, 24.0147, 8.67);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 1714206414810, 40.7675, 24.0145, 10.4);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 1714206415110, 40.7678, 24.0147, 17.33);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (955591b2-061d-449a-9a22-dc9b25557f1c, '2024-04-27', 1714206415411, 40.5197, 24.9761, 17.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (955591b2-061d-449a-9a22-dc9b25557f1c, '2024-04-27', 1714206415511, 40.5191, 24.9764, 25.5);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (0755a898-163e-42fa-b0d3-7354a8e6bdf5, '2024-04-27', 1714206416412, 40.3671, 24.4589, 7.14);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (0755a898-163e-42fa-b0d3-7354a8e6bdf5, '2024-04-27', 1714206416512, 40.3673, 24.4583, 25.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (0755a898-163e-42fa-b0d3-7354a8e6bdf5, '2024-04-27', 1714206416612, 40.3677, 24.4583, 10.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (11112f6b-dfc1-40f8-8248-e272c56f25a0, '2024-04-27', 1714206417313, 40.0464, 24.6475, 16.67);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (11112f6b-dfc1-40f8-8248-e272c56f25a0, '2024-04-27', 1714206417914, 40.0469, 24.6476, 8.33);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (11112f6b-dfc1-40f8-8248-e272c56f25a0, '2024-04-27', 1714206418114, 40.0463, 24.6479, 8.33);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 1714206418314, 40.2572, 24.9596, 10.2);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 1714206418715, 40.2575, 24.9598, 8.5);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 1714206418815, 40.2578, 24.9597, 8.5);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 1714206419716, 40.2571, 24.9595, 10.2);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 1714206420016, 40.2573, 24.9595, 12.75);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (fc56313c-c638-4319-8eaa-5d28321b880b, '2024-04-27', 1714206420517, 40.9907, 24.0636, 25.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (fc56313c-c638-4319-8eaa-5d28321b880b, '2024-04-27', 1714206421417, 40.9902, 24.0636, 25.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (fc56313c-c638-4319-8eaa-5d28321b880b, '2024-04-27', 1714206421818, 40.9904, 24.0633, 16.67);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 1714206422118, 40.6149, 24.8124, 17.33);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 1714206422519, 40.6143, 24.8128, 6.5);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 1714206423220, 40.6148, 24.8121, 6.5);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 1714206423620, 40.6148, 24.8126, 10.4);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (18d0aab9-2834-4ae1-8e45-f6407c79f3eb, '2024-04-27', 1714206424522, 40.3004, 24.2285, 8.5);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (18d0aab9-2834-4ae1-8e45-f6407c79f3eb, '2024-04-27', 1714206425122, 40.3007, 24.2281, 17.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 1714206426023, 40.5939, 24.4916, 26.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 1714206426323, 40.5935, 24.4912, 10.4);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 1714206426623, 40.5931, 24.4914, 8.67);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 1714206426824, 40.5934, 24.4913, 7.43);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 1714206427724, 40.5934, 24.4914, 7.43);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 1714206428625, 40.6856, 24.6054, 7.14);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 1714206428825, 40.6859, 24.6051, 6.25);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 1714206429725, 40.6859, 24.6055, 25.0);
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) 
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 1714206430426, 40.6858, 24.6055, 12.5);
