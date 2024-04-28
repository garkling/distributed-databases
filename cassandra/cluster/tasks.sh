#!/usr/bin/env bash

NODES=("cassandra-1" "cassandra-2" "cassandra-3")

function disconnect_node() {
  docker network disconnect cassandra-cluster cluster-"$1"-1
  echo "[external] $1 disconnected from the cluster"
}

function connect_node() {
    docker network connect cassandra-cluster cluster-"$1"-1
    echo "[external] $1 connected to the cluster"
}

function split_cluster() {
  for node in ${NODES[*]}; do
    disconnect_node "$node"
  done;
  sleep 10
  echo "[external] Inter-node connection lost"
}

function join_cluster() {
  for node in ${NODES[*]}; do
    connect_node "$node"
  done;
  sleep 10
  echo "[external] Inter-node connection restored"
}

function nodetool_status() {
  echo "KEYSPACE: gps_tracking | RF: 3 |  FROM NODE: cassandra-1"
  docker compose exec cassandra-1 bash -c 'nodetool status -- gps_tracking'

  sleep 1
  echo

  echo "KEYSPACE: gps_statistics | RF: 2 | FROM NODE: cassandra-2"
  docker compose exec cassandra-2 bash -c 'nodetool status -- gps_statistics'

  sleep 1
  echo

  echo "KEYSPACE: gps_logging | RF: 1 | FROM NODE: cassandra-3"
  docker compose exec cassandra-3 bash -c 'nodetool status -- gps_logging'
}

function nodetool_endpoints() {
  echo "KEYSPACE: gps_tracking | RF: 3 | TABLE: positions | KEY: fc56313c-c638-4319-8eaa-5d28321b880b | FROM NODE: cassandra-1"
  docker compose exec cassandra-1 bash -c 'nodetool getendpoints -- gps_tracking positions fc56313c-c638-4319-8eaa-5d28321b880b'
  echo "KEYSPACE: gps_tracking | RF: 3 | TABLE: positions | KEY: 3fe73b76-b01d-4502-b2d4-08813a01ef9d | FROM NODE: cassandra-1"
  docker compose exec cassandra-1 bash -c 'nodetool getendpoints -- gps_tracking positions 3fe73b76-b01d-4502-b2d4-08813a01ef9d'

  sleep 1
  echo

  echo "KEYSPACE: gps_statistics | RF: 2 | TABLE: daily_summary | KEY: fc56313c-c638-4319-8eaa-5d28321b880b | FROM NODE: cassandra-2"
  docker compose exec cassandra-2 bash -c 'nodetool getendpoints -- gps_statistics daily_summary fc56313c-c638-4319-8eaa-5d28321b880b'
  echo "KEYSPACE: gps_statistics | TABLE: daily_summary | KEY: 3fe73b76-b01d-4502-b2d4-08813a01ef9d | FROM NODE: cassandra-2"
  docker compose exec cassandra-2 bash -c 'nodetool getendpoints -- gps_statistics daily_summary 3fe73b76-b01d-4502-b2d4-08813a01ef9d'

  sleep 1
  echo

  echo "KEYSPACE: gps_logging | RF: 1 | TABLE: logs | KEY: fc56313c-c638-4319-8eaa-5d28321b880b | FROM NODE: cassandra-3"
  docker compose exec cassandra-3 bash -c 'nodetool getendpoints -- gps_logging logs fc56313c-c638-4319-8eaa-5d28321b880b'
  echo "KEYSPACE: gps_logging | RF: 1 | TABLE: logs | KEY: 3fe73b76-b01d-4502-b2d4-08813a01ef9d | FROM NODE: cassandra-3"
  docker compose exec cassandra-3 bash -c 'nodetool getendpoints -- gps_logging logs 3fe73b76-b01d-4502-b2d4-08813a01ef9d'
}

function rw_consistency_check_with_rf_() {
  cat tasks/rw_consistency_check_rf_"$1.cql"
  echo

  disconnect_node "cassandra-3"
  echo "[external] Waiting for removing the node..."
  sleep 20

  echo
  docker compose exec cassandra-1 bash -c "cqlsh < /tasks/rw_consistency_check_rf_$1.cql"

  connect_node "cassandra-3"
  sleep 10
}

function conflict_resolution_check() {
  split_cluster

  q1="INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3475, 24.2641, 6.25);"
  q2="INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3476, 24.2642, 6.50);"
  q3="INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (a831cd40-132a-4551-bf32-e7f8b1fe9e2e, '2024-04-27', 1714221438626, 40.3477, 24.2643, 6.75);"

  echo "[external] Creating a write conflict between 3 nodes that have no idea about each other"
  echo "[external] cassandra-1 -- $q1"
  echo "[external] cassandra-2 -- $q2"
  echo "[external] cassandra-3 -- $q3"

  docker compose exec cassandra-1 bash -c "cqlsh -k gps_tracking -e \"$q1\""
  docker compose exec cassandra-2 bash -c "cqlsh -k gps_tracking -e \"$q2\""
  docker compose exec cassandra-3 bash -c "cqlsh -k gps_tracking -e \"$q3\""

  join_cluster

  echo "[external] Checking a final applied value. Last write must win"
  docker compose exec cassandra-1 bash -c "cqlsh -k gps_tracking -e \"SELECT * FROM positions WHERE device_id = a831cd40-132a-4551-bf32-e7f8b1fe9e2e AND date = '2024-04-27';\""
}

function lightweight_transaction_check() {

  q1="INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (2ce628ac-419c-4655-b14e-1119ae68c810, '2024-04-27', 1714221438332, 40.3453, 24.2722, 11.25) IF NOT EXISTS;"
  q2="INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (2ce628ac-419c-4655-b14e-1119ae68c810, '2024-04-27', 1714221438332, 40.3443, 24.2723, 12.10) IF NOT EXISTS;"
  q3="INSERT INTO positions (device_id, date, timestamp, latitude, longitude, speed) VALUES (2ce628ac-419c-4655-b14e-1119ae68c810, '2024-04-27', 1714221438332, 40.3433, 24.2723, 13.45) IF NOT EXISTS;"

  echo "[external] Testing lightweight transactions with the same partition key"
  echo "[external] cassandra-1 -- $q1"
  echo "[external] cassandra-2 -- $q2"
  echo "[external] cassandra-3 -- $q3"

  docker compose exec cassandra-1 bash -c "cqlsh -k gps_tracking -e \"$q1\""
  docker compose exec cassandra-2 bash -c "cqlsh -k gps_tracking -e \"$q2\""
  docker compose exec cassandra-3 bash -c "cqlsh -k gps_tracking -e \"$q3\""

  echo "[external] Checking a final applied value. First write must win"
  docker compose exec cassandra-1 bash -c "cqlsh -k gps_tracking -e \"SELECT * FROM positions WHERE device_id = 2ce628ac-419c-4655-b14e-1119ae68c810 AND date = '2024-04-27';\""

  echo '_______________________________________________________________________________________________________________'
  echo "[external] Testing lightweight transactions with the same primary key in a split cluster"
  split_cluster

  echo "[external] Using LWT requires CONSISTENCY SERIAL which is unreachable in a single-node cluster"
  docker compose exec cassandra-1 bash -c "cqlsh -k gps_tracking -e \"$q1\""
  docker compose exec cassandra-2 bash -c "cqlsh -k gps_tracking -e \"$q2\""
  docker compose exec cassandra-3 bash -c "cqlsh -k gps_tracking -e \"$q3\""

  join_cluster
}

funcs=(
nodetool_status
nodetool_endpoints
rw_consistency_check_with_rf_1
rw_consistency_check_with_rf_2
rw_consistency_check_with_rf_3
conflict_resolution_check
lightweight_transaction_check
quit
)

echo "Cluster startup takes approx 6 minutes"
docker compose up -d

PS3="Enter a task number: "
select task in "${funcs[@]}"
do
  case $task in
    "quit")
      break
      ;;
    rw_consistency_check_with_rf_1) rw_consistency_check_with_rf_ 1 ;;
    rw_consistency_check_with_rf_2) rw_consistency_check_with_rf_ 2 ;;
    rw_consistency_check_with_rf_3) rw_consistency_check_with_rf_ 3 ;;
    *)
      eval "$task"
  esac
  echo
done

docker compose down
