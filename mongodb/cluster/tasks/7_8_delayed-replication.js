let db = db.getSiblingDB(process.env.MONGO_DATABASE);
db.getSiblingDB('admin').auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);
let sec_idx = rs.status().members.findIndex((m) => m.stateStr === 'SECONDARY');

cfg = rs.conf();
cfg.members[sec_idx].priority = 0;
cfg.members[sec_idx].hidden = true;
cfg.members[sec_idx].secondaryDelaySecs = 10;
rs.reconfig(cfg);    // configure delayed replication

sleep(1000);
db.documents.insertOne({name: "Write with delayed replication 1", time: Timestamp()}, { writeConcern: {w: 1}});
db.documents.insertOne({name: "Write with delayed replication 2", time: Timestamp()}, { writeConcern: {w: 1}});
db.documents.insertOne({name: "Write with delayed replication 3", time: Timestamp()}, { writeConcern: {w: 1}});
db.documents.find( {name: { $regex: /Write with delayed replication \d/ }} ).readConcern("linearizable");       // should be delayed till replication completes
