# `Cassandra` data modeling and basic operations
### A simple store data model in CQL demonstrating the functionality of indexes, primary keys, and materialized views.
### See [Cluster](cluster) for replication/consistency tests


## Run
Rename `tmp.env` to/create `.env`, you don't need to change anything

If you have `just` command runner:
- `just -l` - list all commands
- `just venv` - create a Python env and install dependencies
- `just help` - show the help for the script execution parameters
- `just start` - start the Docker services (wait approx 6 minutes before any ops)
- `just stop` - stop the Docker services
- `just logs` - show the Docker logs
- `just populate` - populate `items` and `orders` tables 
- `just truncate` - truncate the tables
- `just cqlsh` - run the prepared queries from the `tasks.sh` using the CQL shell (preffered because of tabular output)
- `just run_tasks <tablename>` - run the prepared queries using a `cassandra-driver` dep

Without `just`:
- `ENV_NAME=<env_name>`
- `python3 -m venv $ENV_NAME`
- `source $ENV_NAME/bin/activate`
- `pip install -r requirements.txt`
- use `docker compose up`/`down`/`logs -f` to start/stop/logs the Docker service(s)
- replace `just cqlsh` by `./tasks.sh`  
- replace `just` in the script execution command by `python main.py`
- replace `just run_tasks <tablename>` by `python main.py run_<tablename>_tasks`

## Interaction
#### There are 2 ways to execute tasks: `python` tool or `bash` script
### `bash` (preffered)
The tasks are performed sequentially (see [Tasks](#tasks)).  
You will need to fill in the values yourself in some queries due to the dynamic generation of items UUIDs.   
Manual query formation also serves as a reminder that you have to ensure data consistency yourself on the application side when using Cassandra (e.g. dependence of `order_total` on `items_id`).   
Output in a tabular format.  
Command - `just cqlsh`/`./tasks.sh`

### `python`
The tasks are performed at your choice (see [Tasks](#tasks)).  
Queries are filled in automatically in the Python code, so you will see already prepared queries.  
Output in a list/dict format.  
Command - `just run_tasks <tablename>`/`python main.py run_<tablename>_tasks`
___
#### Also you can execute any query you want in the CQL shell via `just cqlsh_manual`/`sudo docker compose exec -it cassandra-1 cqlsh -k <keyspace from .env>`

## Schema
#### The following snippets are just for better demo, a proper CQL schema is placed in `schema.cql`
### `KEYSPACE store`
### `items`
```cassandraql
category text
brand    text
model    text
price    float
id       uuid
props    map<text, text>

PRIMARY KEY         ( category, brand, model )
INDEX ON KEYS       (props)
INDEX ON ENTRIES    (props)
SASI INDEX ON       (model)
_______________________________________________
MATERIALIZED VIEW items_by_price    PRIMARY KEY ( category, price, brand, model )
MATERIALIZED VIEW items_by_id       PRIMARY KEY ( id, category, brand, model )
```
### `orders`
```cassandraql
customer_name text
order_date    timestamp
order_total   float
id            uuid

items         set<uuid>

PRIMARY KEY     ( customer_name, order_date )
ORDER BY        order_date DESC

INDEX ON VALUES (items)
```

> [!NOTE]
> The CQL schema is applied automatically on the startup by the Docker one-time service `seeder`


## Tasks
#### The list of tasks according to the homework doc
#### `items`
- `00` `get_categories`
- `01` `describe_items`
- `02` `get_items_sorted_by_price`
- `3a` `get_items_by_model`
- `3b` `get_items_by_price_range`
- `3c` `get_items_by_price_by_brand`
- `4a` `get_items_by_property_key`
- `4b` `get_items_by_property_value`
- `5a` `update_item_property`
- `5b` `insert_item_property`
- `5c` `delete_item_property`

#### `orders`
- `00` `get_order_customers`
- `01` `describe_orders`
- `02` `get_orders`
- `03` `get_orders_by_item_id`
- `04` `get_orders_by_date_range`
- `05` `get_orders_total_sum_by_customers`
- `06` `get_max_order_total_by_customers`
- `7a` `insert_order_items`
- `7b` `delete_order_items`
- `08` `get_order_total_writetime`
- `09` `insert_order_ttl`
- `10` `get_orders_in_json`
- `11` `insert_order_json`
