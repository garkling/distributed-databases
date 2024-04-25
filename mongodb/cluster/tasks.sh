#!/usr/bin/env bash

NODES=("mongo-1" "mongo-2" "mongo-3")

function split_cluster() {
  server=$1
  timeout=$2
  docker network disconnect cluster_mongo-cluster cluster-"$server"-1  # cut connection between the selected node and others
  if [ -n "$timeout" ]; then
    echo "[external] $server disconnected from the cluster network for $timeout seconds"
    sleep "$timeout"
    docker network connect cluster_mongo-cluster cluster-"$server"-1
    echo
    echo "[external] $server connected to the cluster network"
  else
    echo "[external] $server disconnected from the cluster network"
  fi

  echo
}

function restart() {
  echo
  echo "[external] re/start the cluster"
  docker compose down
  docker compose up -d
  sleep 30
  echo "[external] cluster is ready"
  echo
}

function get_primary() {
  from=$1
  case $(docker compose exec "$from" bash -c "mongosh --eval 'rs.isMaster().primary'") in
    server1:*) echo "mongo-1" ;;
    server2:*) echo "mongo-2" ;;
    server3:*) echo "mongo-3" ;;
  esac
}


function read_prefs() {
  primary=$(get_primary "mongo-1")
  docker compose exec "$primary" bash -c "mongosh --eval < tasks/2_read-prefs.js"
}

function write_wc_3_no_timeout() {
  primary=$(get_primary "mongo-1")
  secondaries=("${NODES[@]/$primary}")
  split_cluster "${secondaries[2]}" 10 &

  docker compose exec "$primary" bash -c "mongosh --eval < tasks/3_write-with-wc-3-no-timeout.js"
}

function write_wc_3_timeout_10() {
  primary=$(get_primary "mongo-1")
  secondaries=("${NODES[@]/$primary}")

  split_cluster "${secondaries[2]}" 12 &
  docker compose exec "$primary" bash -c "mongosh --eval < tasks/4_write-with-wc-3-timeout-10.js"
}

function primary_elect_reproduce() {
  primary=$(get_primary "mongo-1")
  split_cluster "$primary" 20 &
  echo "[external] a primary node disabled, after 10 second with no response from the primary, the replica set triggers an election"
  sleep 12
  primary=$(get_primary "mongo-2")
  docker compose exec "$primary" bash -c "mongosh --eval < tasks/5_primary-elect-reproduce.js"
}

function inconsistent_state_reproduce() {
  primary=$(get_primary "mongo-1")
  split_cluster "$primary" 12 &
  docker compose exec "$primary" bash -c "mongosh --eval < tasks/6_inconsistent-state-reproduce.js"
}

function delayed_replication() {
  primary=$(get_primary "mongo-1")
  secondaries=("${NODES[@]/$primary}")

  split_cluster "${secondaries[2]}" &
  docker compose exec "$primary" bash -c "mongosh --eval < tasks/7_8_delayed-replication.js"
}

funcs=(
read_prefs
write_wc_3_no_timeout
write_wc_3_timeout_10
primary_elect_reproduce
inconsistent_state_reproduce
delayed_replication
quit
)

PS3="Enter a task number: "
select task in "${funcs[@]}"
do
  case $task in
  "quit")
    break
    ;;
  *)
    restart
    eval "$task"
    wait
    echo
  esac
done
sudo docker compose down
