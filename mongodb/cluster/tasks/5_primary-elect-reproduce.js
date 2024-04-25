let db = db.getSiblingDB(process.env.MONGO_DATABASE);
db.getSiblingDB('admin').auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);

rs.status();
sleep(1000);
db.documents.insertOne(
    {
        name: "After election write",
        time: Timestamp()
    }
);
sleep(8000);
// check data on the ex-primary after re-connection
db.documents.find(
    {name: "After election write"}
).readPref(
    "secondary", [{"name": "server1"}]
).readConcern("majority");
