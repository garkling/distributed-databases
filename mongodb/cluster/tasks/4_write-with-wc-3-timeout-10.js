let db = db.getSiblingDB(process.env.MONGO_DATABASE)
db.auth(process.env.MONGO_DB_USER, process.env.MONGO_DB_PASSWORD);

db.documents.insertOne(
    {
        name: "RS write test",
        wc: 3,
        timeout: 10000,
        time: Timestamp()
    },
    { writeConcern: {w: 3, wtimeout: 10000}}
); // write with WC: 3 and 10s timeout with a disconnected secondary
// check for data before re-connecting the node
db.documents.find({name: "RS write test", wc: 3, timeout: 10000});
db.documents.find({name: "RS write test", wc: 3, timeout: 10000}).readConcern("majority");
sleep(5000);
// check for data after re-connecting the node
db.documents.find({name: "RS write test", wc: 3, timeout: 10000});
db.documents.find({name: "RS write test", wc: 3, timeout: 10000}).readConcern("majority");
