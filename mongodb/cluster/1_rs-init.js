db.getSiblingDB('admin').auth(
    process.env.MONGO_INITDB_ROOT_USERNAME,
    process.env.MONGO_INITDB_ROOT_PASSWORD
);

config = {
      "_id" : "set1",
      "members" : [
          {
              "_id" : 0,
              "host": "server1:27017",
              "tags": {"name": "server1"}
          },
          {
              "_id" : 1,
              "host" : "server2:27017",
              "tags": {"name": "server2"}
          },
          {
              "_id" : 2,
              "host" : "server3:27017",
              "tags": {"name": "server3"}
          }
      ]
}
rs.initiate(config);
