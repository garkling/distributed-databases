let db = db.getSiblingDB(process.env.MONGO_DATABASE)
db.auth(process.env.MONGO_DB_USER, process.env.MONGO_DB_PASSWORD);

db.documents.insertOne({
    name: "readPref",
    time: Timestamp()
});
sleep(1000);
db.documents.find({name: "readPref"}).readPref("primary");
db.documents.find({name: "readPref"}).readPref("secondary");
