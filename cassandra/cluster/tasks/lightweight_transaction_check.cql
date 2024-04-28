USE gps_tracking;

CONSISTENCY ONE;

--- cassandra-1
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed)
VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3475, 24.2641, 6.25)
IF NOT EXISTS;

--- cassandra-2
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed)
VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3476, 24.2642, 6.50)
IF NOT EXISTS;

--- cassandra-3
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed)
VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3477, 24.2643, 6.75)
IF NOT EXISTS;

--- will apply the cassandra-1 write only due to the conditional query, so First Write Wins,
--- but only in a healthy cluster, otherwise all the queries will fail
SELECT * FROM positions WHERE device_id = a831cd40-132a-4551-bf32-e7f8b1fe9e2e AND date = '2024-04-27';
