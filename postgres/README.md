# `PostgreSQL` parallel counter
### Testing of different methods of simultaneous update of a common counter on the Postgres

## Run
Rename `tmp.env` to/create `.env`, and fill in the required args

You can use a local Postgres server of any of the recent versions, or run the Postgres service of the Docker
- If you want to use the Docker service, but have a server running on the host, set `POSTGRES_PORT` other than `5432`

If you have `just` command runner:
- `just -l` - list all commands
- `just venv` - create a Python env and install dependencies
- `just help` - show the help for the script execution parameters
- `just start-postgres` - start the Docker service
- `just stop-postgres` - stop the Docker service
- `just init-db` - drop & create a table `user_counter` (it will init automatically)
- `just <method> <flags>` - run the counter with a specified method
- `just count-all <flags>` - run the counter with all methods in order

Without `just`:
- `ENV_NAME=<env_name>`
- `python3 -m venv $ENV_NAME`
- `source $ENV_NAME/bin/activate`
- `pip install -r requirements.txt`
- use `docker compose up`/`down` to start/stop the Docker service
- replace `just` in the script execution commands by `python main.py --method`
- `python main.py --method <method> <flags>`

Specify `--connections <integer>` to set a number of simultaneous 'connections' (default is `10`)  
Specify `--iters <integer>` to set a number of increment request from each 'connection' (default is `10000`)


## Methods & results
### `lost update`
**Read before write, increment on the client side, no update locks, causes a race condition**

`just count-lost-update`/`python main.py --method lost_update`

With the `--connections 10` and `--iters 10000` the result is close to `10000`, but nondeterministic  
Time `~318 seconds`  
Time range between `1th` and `10th` connection `307-318 seconds`


### `in-place update`
**Direct update attempts, increment on the server side, more reliable**

`just count-in-place-update`/`python main.py --method in_place_update`

With the `--connections 10` and `--iters 10000` the result is `100000`  
Time `~315 seconds`  
Time range between `1th` and `10th` connection `307-315 seconds`


### `row-level locking`
**Explicit update locks, pessimistic locking, increment of the client side**

`just count-row-level-lock`/`python main.py --method row_level_locking`

With the `--connections 10` and `--iters 10000` the result is `100000`  
Time `~335 seconds`  
Time range between `1th` and `10th` connection `330-335 seconds`


### `optimistic concurrency control`
**Involves `version` column (at this case), constant conflict resolution & checks between read and write during high concurrency**

`just count-occ`/`python main.py --method occ`

With the `--connections 10` and `--iters 10000` the result is `100000`  
Time `~2556 seconds`  
Time range between `1th` and `10th` connection `1534-2556 seconds`