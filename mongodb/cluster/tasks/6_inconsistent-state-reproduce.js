let db = db.getSiblingDB(process.env.MONGO_DATABASE);
db.auth(process.env.MONGO_DB_USER, process.env.MONGO_DB_PASSWORD);
// 2 secondaries are disconnected from the primary node at the moment
db.documents.insertOne(
    {
        name: "Inconsistent write",
        time: Timestamp()
    },
    { writeConcern: {w: 1}}
);

db.documents.find({name: "Inconsistent write"}).readConcern("linearizable");    // should not be visible
db.documents.find({name: "Inconsistent write"}).readConcern("majority");        // should not be visible
db.documents.find({name: "Inconsistent write"}).readConcern("local");           // should be visible
sleep(12000); // waiting for a new primary election and restoring connection between members
db.documents.find({name: "Inconsistent write"}); // should disappear
