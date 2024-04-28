# `Cassandra` replication and consistency levels
### Experiments on a 3-node cluster with different RF/CL in different conditions

## Run
Rename `tmp.env` to `.env`, do not change anything

If you have `just` command runner*:
- `just run_tasks` - automatically start cluster and run selected tasks from a list (see [Tasks](#tasks))
- `just cqlsh <server> <keyspace>` - connect to a CQL shell on a specific node to run queries/commands manually
- `just server_bash <server>` - run a command shell inside the node to perform system commands, like `nodetool status`
- `just split_cluster/join_cluster` - disconnect all the cluster nodes from each other/restore connection between the nodes
- `just start/stop/restart/logs` - start/stop/restart/show logs of the Docker services

Without `just`*:
- replace `just run_tasks` by `./tasks.sh`  
- replace `just cqlsh <server> <keyspace>` by `docker compose exec -it <server> bash -c "cqlsh -k <keyspace>"`
- replace `just split_cluster/join_cluster` by applying `docker network disconnect`/`connect cassandra-cluster cluster-<server_name>-1` to each node
- replace `just start/stop/logs` by `docker compose up -d/down/logs`

*(if you got permission issues, use `sudo`)


## Interaction
Just run `just run_tasks`/`./tasks.sh` to begin. There is automatic Docker environment startup, which takes `~6m`  
Such a long startup is caused by the need to fully init the previous node before starting the next one (especially, a seed node)

Choose `1-7` to execute different tasks, `8` to quit.  
During execution, you will see the protocol (`.cql` file if the task requires it) with queries and comments, after which the commands will start executing

> [!IMPORTANT]
> Be sure to check out the `.cql` files for further explanation

The script will destroy the Docker cluster while exiting if you choose `8) quit`.  
You can stop/start the services manually using the above commands.

Check logs by `just logs`/`docker compose logs -f`

Records that you will see them are located in a [`schema/`](schema) folder.  
Task definitions and explanation are localed in a [`tasks/`](tasks) folder.


## Schema
#### For clarity, there are 3 different keyspaces with different degree of data importance - therefore, with different Replication Factors, next `RF`
#### The following snippets are just for better demo, a proper CQL schemas are placed in the [`schema/`](schema) folder

### `KEYSPACE: gps_tracking` `RF: 3`
The most important data representing real-time movement information
#### `positions`
```cassandraql
device_id   UUID
date        DATE
timestamp   BIGINT
latitude    DECIMAL
longitude   DECIMAL
speed       DECIMAL

PRIMARY KEY ( (device_id, date), timestamp)
```
### `KEYSPACE: gps_statistics` `RF: 2`
Important data as well but are derived from original sources, thus can be recovered
#### `daily_summary`
````cassandraql
device_id           UUID
date                DATE
total_distance      DOUBLE
average_speed       DOUBLE
total_tracking_time DOUBLE

PRIMARY KEY         ( device_id, date )
````
### `KEYSPACE gps_logging` `RF: 1`
Metadata that are important only for a certain period of time, and do not represent much value to end users
#### `logs`
```cassandraql
device_id       UUID
date            DATE
level           TEXT
timestamp       BIGINT
message         TEXT

PRIMARY KEY     ( (device_id, date), level, timestamp )
```

## Tasks
1. `Cluster init` - configure a proper 3-node cluster, apply schema and populate by data. Applies automatically on startup
2. `nodetool_status` - check the correct configuration of the cluster and inspect the data distribution across cluster nodes
3. `nodetool_endpoints` - show nodes that own data under a given partition key
4. [`rw_consistency_check_with_rf_1`](tasks/rw_consistency_check_rf_1.cql) - check available consistency levels for read/write for a keyspace `gps_logging` with `RF: 1` during downtime of one of the servers (see expl in the file)
5. [`rw_consistency_check_with_rf_2`](tasks/rw_consistency_check_rf_2.cql) - check available consistency levels for read/write for a keyspace `gps_statistics` with `RF: 2` during downtime of one of the servers (see expl in the file)
6. [`rw_consistency_check_with_rf_3`](tasks/rw_consistency_check_rf_3.cql) - check available consistency levels for read/write for a keyspace `gps_tracking` with `RF: 3` during downtime of one of the servers (see expl in the file)
7. [`conflict_resolution_check`](tasks/conflict_resolution_check.cql) - reproduce a write conflict by splitting the nodes and joining later with different rows under the same primary key (see expl in the file)
8. [`lightweight_transaction_check`](tasks/lightweight_transaction_check.cql) - use lightweight transactions for writes (`IF NOT EXISTS`) in a healthy and split cluster and check results (see expl in the file)


## Note
I cannot directly impact the Casandra partitioner algorithm, therefore, some results may not logically match the description in the task.   
That's because I cannot predict which UUID will belong to which node between restarts - the hash function is the same, but token ranges are always different.  
If something doesn't match, feel free to change a partition key in a task and restart.