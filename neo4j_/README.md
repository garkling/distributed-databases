# `Neo4j` bookstore graph
### A simple bookstore built using nodes and relationships + simple recommendation queries
#### This is an alternative to the homework proposed data model - also based on the online store but with more complex connections and  recommendations based on book purchases and views


## Structure
![bookstore-graph.png](..%2F..%2F..%2F..%2FPictures%2FScreenshots%2Fbookstore-graph.png)
### Node labels
- `Book` - 40 nodes
- `Author` - 32 nodes
- `Genre` - 19 nodes
- `Customer` - 10 nodes
### Relationships
- `WRITTEN_BY` - `Book -> Author`
- `IS_TYPE_OF` - `Book -> Genre`
- `BOUGHT` - `Customer -> Book`
- `VIEWED` - `Customer -> Book`


## Run
Rename `tmp.env` to/create `.env`, and fill in the required args
  - everything is possible, so if your user/groups have an id other than `1000`, please change it in `.env`

Create volume folders in the current folder - `mdkir -p conf/{node1,node2,node3,node4} logs/{node1,node2,node3,node4}`


If you have `just` command runner:
- `just -l` - list all commands
- `just venv` - create a Python env and install dependencies
- `just help` - show the help for the script execution parameters
- `just start` - start the Docker services (wait a few minutes at the first start)
- `just stop` - stop the Docker services
- `just logs` - show the Docker logs
- `just create-graph` - create the bookstore Graph from `cypher/BOOKSTORE_GRAPH.cypher`
- `just delete-graph` - delete the graph
- `just run` - run the interactive query executor with prepared queries

Without `just`:
- `ENV_NAME=<env_name>`
- `python3 -m venv $ENV_NAME`
- `source $ENV_NAME/bin/activate`
- `pip install -r requirements.txt`
- use `docker compose up`/`down`/`logs -f` to start/stop/logs the Docker service(s)
- replace `just` in the script execution command by `python main.py`

#### Note
The current environment contains a `pyvis` lib for drawing graphs, and has a lot of dependencies. If you don't want to install it, remove from the `requirements.txt`. Later, during the execution, do not choose `graph` as an output format  
You can view graphs via `Neo4j Browser`, graph-return queries are stored in `queries.py` in `queries` dict under the key `'graph'` 

## Interaction methods
### `CLI`
After `just run`/`python main.py run`, you will see a numbered list of prepared cases each triggers a specific query:
- choose a number within `[1-16]`
- specify whether you want an output in a `graph` form (default is `table`) - skip for the default format
  - you can choose the output format for almost all queries, except aggregation/reduce ones which results are only tabular
- some queries require a value to be passed to them for execution, in which case you will be prompted to enter this value. 
  - it may be a `Customer`/`Book`/`Author` name or a simple `YYYY-MM-DD` format date - the prompt message will hint what to enter.
- contemplate the result of execution
- repeat the procedure with a new number
- leave the number prompt empty to exit, or enter `h` to output the cases list
### `UI` `Neo4j Browser`
You also can use the built-in `Neo4j` console on your host at the [`http://localhost:7474/browser/`](http://localhost:7474/browser/)  
- log in with the creds from `NEO4J_AUTH` (`<username>/<password>`)
- enter your queries or drag-n-drop `*.cypher` files from the `cypher/` folder - you can immediately add them to `Favorites` for quick access
- run by `Ctrl+Enter` or pressing the play button and choose the desired output format
  - the graph view will be available only if you return whole node objects (`RETURN book`) instead of their properties (`RETURN book.title`)
  - get the whole graph by running `MATCH (n) RETURN n`
  - delete the graph by running `MATCH (n) DETACH DELETE n`

## Queries
#### General
- `get_all`/`get_all_*` - get all nodes with a specified `*` label, including a useful aggregations and info about neighboring nodes

#### `Customer`-centric
- `get_customer_orders_info` - all customer's orders with the date and price
- `get_customer_orders_grouped_by_date` - the same as above grouped by date
- `get_viewed_books_by_customer` - all customer's viewed books including bought ones
- `get_viewed_not_bought_books_by_customer` - the same as above excluding bought books
- `sum_price_for_customer` - calculate the total amount of money spent for the entire period

#### `Book`-centric
- `get_books_bought_together_with_book` - find books being purchased with the specified one on the same date
- `get_customer_info_by_book_ordered` - find customers who bought the specified book
- `group_books_by_times_bought` - grouping by the number of book orders (without specifying a book name)


#### By date
- `get_orders_by_date` - find orders that were made on this date + customer info

#### Recommendations (for customers)
- `recommend_same_author_books_by_viewed` - recommend books by the same author whose books were previously viewed by the customer. 
  - The more an author's books have been viewed, the stronger the recommendation for that author's books.
- `recommend_similar_books_based_on_customer_orders` - recommend books of the same genre that the customer bought books before. 
  - genres that the customer has the most will be recommended first


## Notes
1) Feel free to write own queries/create new nodes and relations via `Neo4j Browser`
2) Numbered queries in the `cypher/` folder refer to similar tasks in the homework document