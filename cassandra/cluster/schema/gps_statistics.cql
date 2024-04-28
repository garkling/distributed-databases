-- important data but are derived from original sources, thus can be recovered
CREATE KEYSPACE IF NOT EXISTS gps_statistics
    WITH REPLICATION = {
        'class': 'SimpleStrategy',
        'replication_factor': 2
        };

USE gps_statistics;

CREATE TABLE IF NOT EXISTS daily_summary
(
    device_id           UUID,
    date                DATE,
    total_distance      DOUBLE,
    average_speed       DOUBLE,
    total_tracking_time DOUBLE,
    PRIMARY KEY ( device_id, date )
);

INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (3fe73b76-b01d-4502-b2d4-08813a01ef9d, '2024-04-27', 2.0, 15.6, 1.70198);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (955591b2-061d-449a-9a22-dc9b25557f1c, '2024-04-27', 0.67, 21.25, 1.00074);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (0755a898-163e-42fa-b0d3-7354a8e6bdf5, '2024-04-27', 0.88, 14.05, 0.90108);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (11112f6b-dfc1-40f8-8248-e272c56f25a0, '2024-04-27', 1.0, 11.11, 1.00123);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (0b30dee6-26fc-4f35-89c0-7557932bdcc5, '2024-04-27', 0.67, 10.03, 2.20265);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (fc56313c-c638-4319-8eaa-5d28321b880b, '2024-04-27', 2.5, 22.22, 1.60137);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (030e0c63-5a9c-40bf-8a37-a6b1f8cc93bc, '2024-04-27', 1.14, 10.18, 2.40298);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (18d0aab9-2834-4ae1-8e45-f6407c79f3eb, '2024-04-27', 0.83, 12.75, 1.50109);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (4040161a-a307-426b-ac72-e1f052a3d7df, '2024-04-27', 1.0, 11.99, 2.60199);
INSERT INTO daily_summary (device_id, date, total_distance, average_speed, total_tracking_time) 
VALUES (a41588e2-fe43-4c3e-b163-14d5da1a2342, '2024-04-27', 0.8, 12.72, 2.1019);
