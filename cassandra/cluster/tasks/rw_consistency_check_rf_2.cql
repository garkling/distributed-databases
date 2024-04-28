-- SITUATION: 2/3 of nodes is alive
-- REPLICATION FACTOR: 2

USE gps_statistics;

CONSISTENCY ALL;
-- with RP: 2, CONSISTENCY ALL = QUORUM = TWO
-- allows to write, only in case if
-- - a new partition key being inserted happens to hit only alive nodes based on a token range (data will replicate on alive nodes)
-- - an existing partition key which is stored on alive nodes is being inserted
-- allows to read, only in case if
-- - a partition key which is stored on alive nodes is being queried

-- one of these read/writes will not work due to a partitioning algorithm
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c61, '2024-04-27', 3.2, 8.5, 2.10);
SELECT * FROM daily_summary WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c61 AND date = '2024-04-27';

INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c60, '2024-04-27', 3.3, 1.3, 1.30);
SELECT * FROM daily_summary WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c60 AND date = '2024-04-27';

-- some of these reads are unreachable because a row is stored on a dead replica
SELECT * FROM daily_summary WHERE device_id = a41588e2-fe43-4c3e-b163-14d5da1a2342 AND date = '2024-04-27';
SELECT * FROM daily_summary WHERE device_id = 3fe73b76-b01d-4502-b2d4-08813a01ef9d AND date = '2024-04-27';
SELECT * FROM daily_summary WHERE device_id = 4040161a-a307-426b-ac72-e1f052a3d7df AND date = '2024-04-27';

CONSISTENCY ONE; -- will work, but provides only eventual consistency
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c61, '2024-04-27', 3.2, 8.5, 2.10);
SELECT * FROM daily_summary WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c61 AND date = '2024-04-27';


-- UNAVAILABLE:             THREE
-- STRONG CONSISTENCY:      ALL/QUORUM/TWO (under the above conditions)
-- EVENTUAL CONSISTENCY:    ONE/ANY
