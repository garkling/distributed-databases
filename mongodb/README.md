# `MongoDB` query translator using Python operators and methods
### A utility designed to interact with MongoDB using [`pymongo`](https://pypi.org/project/pymongo/) by leveraging Python's operator overloading mechanism to translate Python conditional statements into MongoDB queries.

## Modes

### **Playground / query executor**
Query/modify/drop any collection you want  
`just <operation> <collection> [--filename] [--params <KEY=VALUE>]` or  
`python main.py <operation> <collection> [--filename] [--params <KEY=VALUE>]`

Use `--filename <value>` with the `insert_many` operation  
Add `--params` for the custom collection creation, e.g `--params capped=True size=10000 max=5` for the capped collection

#### Operations
Applies to a specified collection:
- `insert_many` - insert from the `json` file
- `insert` - interactively insert a single document at the time
- `get` - interactively query any documents you need (empty query matches all documents)
- `update` - interactively specify a query to match documents (empty query matches all documents) & next specify an update query to select the fields to change
- `remove` - interactively specify a query to remove matched documents (empty query matches all documents, so removes the all!)
- `drop` - just drop the collection

Without specifying a collection:
- `populate` - populate the `items`/`orders` collections with the prepared data

___
### **Task executor**
Perform tasks on the set of collections (intended for checking homework)  
`just task <items/orders/last_reviews> [--record]` or  
`python tasks.py <items/orders/last_reviews> [--record]`

Use `--record` if you want to observe logs later in the file `./<collection_name>_tasks.log`


## Run
Rename `tmp.env` to/create `.env`, and fill in the required args
- `MONGO_INITDB_DATABASE` better be the same as `MONGO_DATABASE`

If you have `just` command runner:  
- `just -l` - to list all commands
- `just venv` - to create a Python env and install dependencies
- `just start-mongo` to start Docker service
- `just stop-mongo` to stop Docker service
- `just help` to show the help for the MongoDB client wrapper & task executor
- `just populate` - populate the `items`/`orders` collections (initial items are stored in `items.json`)
- `just <operation> <collection> <flags>` - to apply the operation for the given collection (see [Operation](#operations) section)

Without `just`:
- `ENV_NAME=<env_name>`
- `python3 -m venv $ENV_NAME`
- `source $ENV_NAME/bin/activate`
- `pip install -r requirements.txt`
- replace `just` in the command by `python main.py` for running the query executor (see [Query executor](#playground--query-executor) section)
- replace `just task` in the command by `python tasks.py` for executing prepared tasks (see [Task executor](#task-executor) section)

When you execute the command, depending on the selected operation, you will see one or more input prompts one after the other.  
Use [Syntax](#syntax) chapter for reference


## Syntax

### Query syntax examples:
Pure operators:
- `category ==`/`!= 'TV'` - analog of `$eq`/`$ne` operator
- `price >`/`>=`/`<`/`<= 300` - analog of `$gt`/`$gte`/`$lt`/`$lte` operator
- `(category == 'TV') &`/`| (price >= 300)` - analog of `$and`/`$or` operator
- `customer.phones[0] == 8489093` - access to fields in embedded documents/array items by index

Field methods:
- `brand.in_`/`nin(<values separated by comma>)` - analog of `$in`/`$nin` operator
- `price.between(1000,2000)`/`(price > 1000) & (price < 2000)` - equivalent to `price: {$gt: 1000, $lt: 2000}`
- `water_resistance.exists`/`not_exists()` - analog of `$exists: True`/`False` statement

Grouping/aggregation methods:
- `brand.distinct([<fields separated by comma>])` - get distinct documents by `<*fields>` if given else by `brand`
- `brand.count([<field>])` - get number of documents by `<field>` if given else by `brand`
- `brand.in_('Apple', 'Samsung').distinct().count()` - you can chain methods together
- `(model == 'iPhone 13').count()` - you can apply the methods to queries as well

Joins:
- `<local_field>.join('<foreign_collection>.<foreigh_field>'[, on='<local_field if <query>.join()>'][, where="<query on foreign fields>"][, alias='<name of joined document>'])`
- `items_id.join('items._id')` - joins made by `$lookup` operator (`items_id` contains reference ids)
- `(date.between('2024-01-01', '2024-12-31')).join('items._id'])` - you can join query result, but have to specify `on` field
- `(date.between('2024-01-01', '2024-12-31')).join('items._id', on='items_id', where="brand == 'Apple'", alias='apple_ordered')` - by specifying `where`, you can query on foreign collection as well

You can chain and combine all the methods in any order, play with operators, make long complex queries - MongoDB engine itself will discard weird/invalid ones

`+ -` operators are now allowed here

### Update query syntax examples:
- `model == 'iPhone 13'` - analog of `$set` operator
- `model.unset()'` - analog of `$unset` operator
- `price +`/`- 300` - analog of `$inc` operator
- `total_sum * 0.8` - analog of `$mul` operator
- `customer.phones +`/`- [41...]` - analog of `$push`/`$pull` array operators
- `(price + 300) & (warranty == '5 years')` - join multiple update statements (enclose each statement in parentheses)
- `items_id - [ordered[0]['_id']]` - you can reference fields returned by searching query, handy after `.join`ing (currently, it works poorly and is unstable)

You are able to not only modify the existing fields, but specify a new ones with any value

`| > >= < <=` operators are now allowed here

### Projection
After entering the query in `get` operation, you can also specify the fields you want to see in the result.  
- leave empty to display the fields that appeared in the query
- enter `all` to display all the fields available
- enter any number of fields to display only these, e.g. `category,brand,model,price` or `customer.name,payment.cardId` for embedded documents


## Limitations
This program was developed as part of a homework project and is therefore not intended for use in environments other than this type.  
The query executor covers only basic MongoDB operations - it is not able to properly perform complex multi-stage grouping and aggregations, has no read/write preference/concerns, index creation and others...
Given the above, at the moment, the tool is only suitable for the introduction to MongoDB functionality in a single-server local environment.
