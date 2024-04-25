let db = db.getSiblingDB(process.env.MONGO_DATABASE)
db.auth(process.env.MONGO_DB_USER, process.env.MONGO_DB_PASSWORD);

db.documents.insertOne(
    {
        name: "RS write test",
        wc: 3,
        timeout: null,
        time: Timestamp()
    },
    { writeConcern: {w: 3}}
);  // write with WC: 3 with a disconnected secondary
// re-connecting the node...
db.documents.find({name: "RS write test", wc: 3, timeout: null});
db.documents.find({name: "RS write test", wc: 3, timeout: null}).readConcern("majority");
