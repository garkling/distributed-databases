-- SITUATION: 2/3 of nodes is alive
-- REPLICATION FACTOR: 1

USE gps_logging;

CONSISTENCY ALL;
-- with RP: 1, CONSISTENCY ALL = QUORUM = ONE, because of 1 replica
-- allows to write, only in case if
-- - a new partition key being inserted happens to hit one of the alive nodes based on a token range
-- - an existing partition key which is stored on alive nodes is being inserted
-- allows to read, only in case if
-- - a partition key which is stored on alive nodes is being queried

-- one of these read/writes may not work due to a partitioning algorithm
INSERT INTO logs (device_id, date, level, timestamp, message) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c61, '2024-04-27', 'INFO', 1714221421877, '[INFO][1714221421877] - {id: e99b2c16-884f-4139-ad60-31d8ca589c61, pos: (40.2174, 24.9468), acc: 10.4}');
SELECT * FROM logs WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c61 AND date = '2024-04-27';

INSERT INTO logs (device_id, date, level, timestamp, message) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c60, '2024-04-27', 'INFO', 1714221421877, '[INFO][1714221421877] - {id: e99b2c16-884f-4139-ad60-31d8ca589c61, pos: (40.2174, 24.9468), acc: 10.4}');
SELECT * FROM logs WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c60 AND date = '2024-04-27';

-- some of these keys are stored on the dead node, so will be unreachable
SELECT * FROM logs WHERE device_id = a41588e2-fe43-4c3e-b163-14d5da1a2342 AND date = '2024-04-27';
SELECT * FROM logs WHERE device_id = 3fe73b76-b01d-4502-b2d4-08813a01ef9d AND date = '2024-04-27';
SELECT * FROM logs WHERE device_id = 4040161a-a307-426b-ac72-e1f052a3d7df AND date = '2024-04-27';

SELECT * FROM logs; -- will not work under any circumstances

CONSISTENCY ANY;
-- allows to write, even if a replica node for the given partition key is down, using hinted handoff mechanism
-- reads do not work at this level
INSERT INTO logs (device_id, date, level, timestamp, message) VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 'INFO', 1714221442563, '[INFO][1714221442563] - {id: a41588e2-fe43-4c3e-b163-14d5da1a2342, pos: (40.4122, 24.3934), acc: 3.8}');
SELECT * FROM logs WHERE device_id = a41588e2-fe43-4c3e-b163-14d5da1a2342 AND date = '2024-04-27';

CONSISTENCY TWO;
-- with RP: 1, makes no sense, as well as CONSISTENCY THREE
INSERT INTO logs (device_id, date, level, timestamp, message) VALUES (e99b2c16-884f-4139-ad60-31d8ca589c61, '2024-04-27', 'INFO', 1714221421877, '[INFO][1714221421877] - {id: e99b2c16-884f-4139-ad60-31d8ca589c61, pos: (40.2174, 24.9468), acc: 10.4}');
SELECT * FROM logs WHERE device_id = e99b2c16-884f-4139-ad60-31d8ca589c61 AND date = '2024-04-27';


-- UNAVAILABLE:             TWO/THREE
-- STRONG CONSISTENCY:      ALL/QUORUM/ONE (under the above conditions)
-- EVENTUAL CONSISTENCY:    ANY
