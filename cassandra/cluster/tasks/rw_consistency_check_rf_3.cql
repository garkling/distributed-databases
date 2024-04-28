-- SITUATION: 2/3 of nodes is alive
-- REPLICATION FACTOR: 3

USE gps_tracking;

CONSISTENCY ALL; -- or THREE, unavailable because of not enough alive replicas
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c61, '2024-04-27', 1714221422209, 40.2174, 24.9468, 10.4);
SELECT * FROM positions WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c61 AND date = '2024-04-27';

CONSISTENCY QUORUM; -- or TWO, will work because in this case quorum is the number of alive replicas
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c61, '2024-04-27', 1714221422209, 40.2174, 24.9468, 10.4);
SELECT * FROM positions WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c61 AND date = '2024-04-27';
SELECT * FROM positions;

CONSISTENCY ONE; -- will work either, but provides eventual consistency for this particular read/write pair
INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c61, '2024-04-27', 1714221423511, 40.2177, 24.9469, 6.5);
SELECT * FROM positions WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c61 AND date = '2024-04-27';


-- UNAVAILABLE:             ALL/THREE
-- STRONG CONSISTENCY:      QUORUM/TWO
-- EVENTUAL CONSISTENCY:    ONE
