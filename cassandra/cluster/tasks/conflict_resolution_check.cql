USE gps_tracking;

CONSISTENCY ONE;

--- cassandra-1
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed)
VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3475, 24.2641, 6.25);

--- cassandra-2
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed)
VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3476, 24.2642, 6.50);

--- cassandra-3
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed)
VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3477, 24.2643, 6.75);

--- uses LWW (Last Write Win) to resolve the conflict, so the cassandra-3 write will be applied
SELECT * FROM positions WHERE device_id = a831cd40-132a-4551-bf32-e7f8b1fe9e2e AND date = '2024-04-27';
