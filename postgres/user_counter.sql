DROP TABLE IF EXISTS user_counter;

CREATE TABLE user_counter (
    user_id INT,
    counter INT DEFAULT 0,
    version INT DEFAULT 1
);

INSERT INTO user_counter (user_id)
VALUES (1);
