-- least important metadata
CREATE KEYSPACE IF NOT EXISTS gps_logging
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE gps_logging;

CREATE TABLE IF NOT EXISTS logs
(
    device_id UUID,
    date      DATE,
    level     TEXT,
    timestamp BIGINT,
    message   TEXT,
    PRIMARY KEY ( (device_id, date), level, timestamp )
);

INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 'INFO', 1714206413136, '[INFO][1714206413136] - {id: 3fe73b76-b01d-4502-b2d4-08813a01ef9d, pos: (40.7677, 24.0141), acc: 26.0}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 'INFO', 1714206413931, '[INFO][1714206413931] - {id: 3fe73b76-b01d-4502-b2d4-08813a01ef9d, pos: (40.7677, 24.0147), acc: 8.67}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 'INFO', 1714206414180, '[INFO][1714206414180] - {id: 3fe73b76-b01d-4502-b2d4-08813a01ef9d, pos: (40.7675, 24.0145), acc: 10.4}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 'INFO', 1714206414801, '[INFO][1714206414801] - {id: 3fe73b76-b01d-4502-b2d4-08813a01ef9d, pos: (40.7678, 24.0147), acc: 17.33}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (955591b2-061d-449a-9a22-dc9b25557f1c, '2024-04-27', 'INFO', 1714206415094, '[INFO][1714206415094] - {id: 955591b2-061d-449a-9a22-dc9b25557f1c, pos: (40.5197, 24.9761), acc: 17.0}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (955591b2-061d-449a-9a22-dc9b25557f1c, '2024-04-27', 'INFO', 1714206414854, '[INFO][1714206414854] - {id: 955591b2-061d-449a-9a22-dc9b25557f1c, pos: (40.5191, 24.9764), acc: 25.5}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (0755a898-163e-42fa-b0d3-7354a8e6bdf5, '2024-04-27', 'INFO', 1714206415805, '[INFO][1714206415805] - {id: 0755a898-163e-42fa-b0d3-7354a8e6bdf5, pos: (40.3671, 24.4589), acc: 7.14}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (0755a898-163e-42fa-b0d3-7354a8e6bdf5, '2024-04-27', 'INFO', 1714206416147, '[INFO][1714206416147] - {id: 0755a898-163e-42fa-b0d3-7354a8e6bdf5, pos: (40.3673, 24.4583), acc: 25.0}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (0755a898-163e-42fa-b0d3-7354a8e6bdf5, '2024-04-27', 'INFO', 1714206416275, '[INFO][1714206416275] - {id: 0755a898-163e-42fa-b0d3-7354a8e6bdf5, pos: (40.3677, 24.4583), acc: 10.0}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (11112f6b-dfc1-40f8-8248-e272c56f25a0, '2024-04-27', 'INFO', 1714206416851, '[INFO][1714206416851] - {id: 11112f6b-dfc1-40f8-8248-e272c56f25a0, pos: (40.0464, 24.6475), acc: 16.67}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (11112f6b-dfc1-40f8-8248-e272c56f25a0, '2024-04-27', 'INFO', 1714206417266, '[INFO][1714206417266] - {id: 11112f6b-dfc1-40f8-8248-e272c56f25a0, pos: (40.0469, 24.6476), acc: 8.33}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (11112f6b-dfc1-40f8-8248-e272c56f25a0, '2024-04-27', 'INFO', 1714206417802, '[INFO][1714206417802] - {id: 11112f6b-dfc1-40f8-8248-e272c56f25a0, pos: (40.0463, 24.6479), acc: 8.33}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 'INFO', 1714206417987, '[INFO][1714206417987] - {id: 0b30dee6-26fc-4f35-89c0-7557932bdcc5, pos: (40.2572, 24.9596), acc: 10.2}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 'INFO', 1714206417942, '[INFO][1714206417942] - {id: 0b30dee6-26fc-4f35-89c0-7557932bdcc5, pos: (40.2575, 24.9598), acc: 8.5}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 'INFO', 1714206418358, '[INFO][1714206418358] - {id: 0b30dee6-26fc-4f35-89c0-7557932bdcc5, pos: (40.2578, 24.9597), acc: 8.5}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 'INFO', 1714206419362, '[INFO][1714206419362] - {id: 0b30dee6-26fc-4f35-89c0-7557932bdcc5, pos: (40.2571, 24.9595), acc: 10.2}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 'INFO', 1714206419341, '[INFO][1714206419341] - {id: 0b30dee6-26fc-4f35-89c0-7557932bdcc5, pos: (40.2573, 24.9595), acc: 12.75}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (fc56313c-c638-4319-8eaa-5d28321b880b, '2024-04-27', 'INFO', 1714206419926, '[INFO][1714206419926] - {id: fc56313c-c638-4319-8eaa-5d28321b880b, pos: (40.9907, 24.0636), acc: 25.0}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (fc56313c-c638-4319-8eaa-5d28321b880b, '2024-04-27', 'INFO', 1714206421001, '[INFO][1714206421001] - {id: fc56313c-c638-4319-8eaa-5d28321b880b, pos: (40.9902, 24.0636), acc: 25.0}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (fc56313c-c638-4319-8eaa-5d28321b880b, '2024-04-27', 'INFO', 1714206421165, '[INFO][1714206421165] - {id: fc56313c-c638-4319-8eaa-5d28321b880b, pos: (40.9904, 24.0633), acc: 16.67}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 'INFO', 1714206421738, '[INFO][1714206421738] - {id: 030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, pos: (40.6149, 24.8124), acc: 17.33}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 'INFO', 1714206421757, '[INFO][1714206421757] - {id: 030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, pos: (40.6143, 24.8128), acc: 6.5}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 'INFO', 1714206422727, '[INFO][1714206422727] - {id: 030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, pos: (40.6148, 24.8121), acc: 6.5}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 'INFO', 1714206423189, '[INFO][1714206423189] - {id: 030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, pos: (40.6148, 24.8126), acc: 10.4}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (18d0aab9-2834-4ae1-8e45-f6407c79f3eb, '2024-04-27', 'INFO', 1714206423825, '[INFO][1714206423825] - {id: 18d0aab9-2834-4ae1-8e45-f6407c79f3eb, pos: (40.3004, 24.2285), acc: 8.5}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (18d0aab9-2834-4ae1-8e45-f6407c79f3eb, '2024-04-27', 'INFO', 1714206424237, '[INFO][1714206424237] - {id: 18d0aab9-2834-4ae1-8e45-f6407c79f3eb, pos: (40.3007, 24.2281), acc: 17.0}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 'INFO', 1714206425227, '[INFO][1714206425227] - {id: 4040161a-a307-426b-ac72-e1f052a3d7df, pos: (40.5939, 24.4916), acc: 26.0}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 'INFO', 1714206425590, '[INFO][1714206425590] - {id: 4040161a-a307-426b-ac72-e1f052a3d7df, pos: (40.5935, 24.4912), acc: 10.4}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 'INFO', 1714206425859, '[INFO][1714206425859] - {id: 4040161a-a307-426b-ac72-e1f052a3d7df, pos: (40.5931, 24.4914), acc: 8.67}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 'INFO', 1714206426101, '[INFO][1714206426101] - {id: 4040161a-a307-426b-ac72-e1f052a3d7df, pos: (40.5934, 24.4913), acc: 7.43}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 'INFO', 1714206426902, '[INFO][1714206426902] - {id: 4040161a-a307-426b-ac72-e1f052a3d7df, pos: (40.5934, 24.4914), acc: 7.43}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 'INFO', 1714206427830, '[INFO][1714206427830] - {id: a41588e2-fe43-4c3e-b163-14d5da1a2342, pos: (40.6856, 24.6054), acc: 7.14}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 'INFO', 1714206428007, '[INFO][1714206428007] - {id: a41588e2-fe43-4c3e-b163-14d5da1a2342, pos: (40.6859, 24.6051), acc: 6.25}');
INSERT INTO logs (device_id, date, level, timestamp, message) 
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 'INFO', 1714206428889, '[INFO][1714206428889] - {id: a41588e2-fe43-4c3e-b163-14d5da1a2342, pos: (40.6859, 24.6055), acc: 25.0}');
INSERT INTO logs (device_id, date, level, timestamp, message)
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 'INFO', 1714206430123, '[INFO][1714206430123] - {id: a41588e2-fe43-4c3e-b163-14d5da1a2342, pos: (40.6858, 24.6055), acc: 12.5}');
