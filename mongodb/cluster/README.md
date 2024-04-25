# `MongoDB` replication and fault tolerance test
### Experiments on a P-S-S replica set

## Run
Rename `tmp.env` to/create `.env`, and fill in the required args
- `MONGO_INITDB_DATABASE` better be the same as `MONGO_DATABASE`

Run `mkdir logs/ && touch logs/server{1,2,3}.log` to create a logfile for each node

Run `sudo chown 999:999 mongodb.key` for MongoDB to use this key in replica set communication (`999` is your docker user's id) 

If you have `just` command runner*:
- `just run_tasks` - automatically start cluster and run selected tasks from a list (see [Tasks](#tasks))
- `just mongosh <server>` - connect to a Mongo shell on a specific server to run queries/commands manually
- `just start/stop/restart/logs` - start/stop/restart/show logs of the Docker services

Without `just`*:
- replace `just run_tasks` by `./tasks.sh`  
- replace `just mongosh <server>` by `docker compose exec -it <server> mongosh`
- replace `just start/stop/logs` by `docker compose up -d/down/logs`

*(if you got permission issues, use `sudo`)


## Interaction
Just run `just run_tasks`/`./tasks.sh` to begin. There is automatic Docker environment startup, which takes `~30s`  
Choose `1-6` to execute different tasks, `7` to quit.  

After the task is executed, a complete restart occurs - re-deploying services and initializing a replica set takes `~1m`  
The restart between tasks is necessary to prevent the impact of previous operations.  
Also the script will destroy the Docker services while exiting if you choose `7) quit`.

You can stop/start the services manually using the above commands.  
Check logs by `less logs/*`

## Tasks
1. [`RS init`](1_rs-init.js) - configure a [P-S-S](https://www.mongodb.com/docs/manual/core/replica-set-architecture-three-members/#three-member-replica-sets) replica set. Applies automatically on startup
2. [`read_prefs`](tasks/2_read-prefs.js) - test document reads with `primary`/`secondary` read preferences
3. [`write_wc_3_no_timeout`](tasks/3_write-with-wc-3-no-timeout.js) - test writes with 1 disconnected secondary, `writeConcern: 3` and infinite timeout
4. [`write_wc_3_timeout_10`](tasks/4_write-with-wc-3-timeout-10.js) - test writes with 1 disconnected secondary, `writeConcern: 3` and `10s` timeout
5. [`primary_elect_reproduce`](tasks/5_primary-elect-reproduce.js) - reproduce a situation which causes a replica set to elect a new primary, also check data replication on the reconnected ex-primary node
6. [`inconsistent_state_reproduce`](tasks/6_inconsistent-state-reproduce.js) - reproduce an inconsistent state when a primary writes separately from secondaries, and after normalizing the replica set, data disappears
7. [`delayed_replication`](tasks/7_8_delayed-replication.js) - configure delayed replication with 1 disconnected secondary, and experience delay when reading data while replication is in progress
