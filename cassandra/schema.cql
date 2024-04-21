CREATE KEYSPACE IF NOT EXISTS store
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};
USE store;

CREATE TABLE IF NOT EXISTS items
(
    category text,
    brand    text,
    model    text,
    price    float,
    id       uuid,

    props    map<text, text>,
    PRIMARY KEY ( category, brand, model )
);

CREATE INDEX IF NOT EXISTS props_k_idx ON items (ENTRIES (props));
CREATE INDEX IF NOT EXISTS props_v_idx ON items (KEYS (props));

--- Full text search by model name
CREATE CUSTOM INDEX IF NOT EXISTS model_idx ON items (model)
USING 'org.apache.cassandra.index.sasi.SASIIndex'
WITH OPTIONS = {
    'mode': 'CONTAINS',
    'analyzer_class': 'org.apache.cassandra.index.sasi.analyzer.NonTokenizingAnalyzer',
    'case_sensitive': 'false'
};

--- For price ranges search by category
CREATE MATERIALIZED VIEW IF NOT EXISTS items_by_price AS
SELECT *
FROM items
WHERE category IS NOT NULL
  AND price IS NOT NULL
  AND brand IS NOT NULL
  AND model IS NOT NULL
PRIMARY KEY ( category, price, brand, model );

--- For access to the item info by its id (e.g. in orders)
CREATE MATERIALIZED VIEW IF NOT EXISTS items_by_id AS
SELECT *
FROM items
WHERE category IS NOT NULL
  AND id IS NOT NULL
  AND brand IS NOT NULL
  AND model IS NOT NULL
PRIMARY KEY ( id, category, brand, model );


CREATE TABLE IF NOT EXISTS orders
(
    customer_name text,
    order_date    timestamp,
    order_total   float,
    id            uuid,

    items         set<uuid>,
    PRIMARY KEY (customer_name, order_date)
) WITH CLUSTERING ORDER BY (order_date DESC);

CREATE INDEX item_idx ON orders (VALUES (items));
