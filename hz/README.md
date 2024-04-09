# `Hazelcast` concurrent counter increment
### Testing of different locking strategies and structures for incrementing a distributed counter in Hazelcast cluster


## Setup
### Cloud + Kubernetes
I used 3-node **GKE** cluster with `cpSubsystem` enabled, which requires the `hazelcast-enterprise` image, which requires a license key)  
You can setup Kubernetes in any cloud  
You can also specify your cloud in `hazelcast-config.yaml` `hazelcast.network.join` to configure discovery strategies

1. `gcloud container clusters get-credentials <CLUSTER_NAME> --zone <REGION> --project <PROJECT_ID>` for `GKE`
2. `helm repo add hazelcast https://hazelcast-charts.s3.amazonaws.com` - for testing in a true production-like deployment, use `helm` charts
3. `helm repo update`
4. `kubectl create namespace hazelcast-ns`
5. `kubectl -n hazelcast-ns create configmap hazelcast-config --from-file=hazelcast-config.yaml`

6. ##### If you have an Enterprise key (you can get Trial):
   1. `helm install operator hazelcast/hazelcast-platform-operator --version=5.11.0-snapshot --set=installCRDs=true`
      - use `--version=5.11.0-snapshot` or later to get `cpSubsystem` API in the operator
   2. `kubectl -n hazelcast-ns create secret generic hazelcast-license-key --from-literal=license-key=<your-key>`
   3. `kubectl apply -f hazelcast-enterprise.yaml`
       - the manifest already has `cpSubsystem` + `pvc` configured, you can remove the `cpSubsystem` block

6. ##### Open Source version:
   1. `helm install operator hazelcast/hazelcast-platform-operator --version=5.10.0 --set=installCRDs=true`
   2. `kubectl apply -f hazelcast.yaml`
___
7. `kubectl -n hazelcast-ns get hazelcast`
8. `kubectl -n hazelcast-ns get hazelcastendpoint -l app.kubernetes.io/instance=hazelcast`
   - it will output `hazelcast  Discovery   <cluster-endpoint>`, set `HZ_CLUSTER_MEMBERS=<cluster-endpoint>` in `.env` 
9. `kubectl -n hazelcast-ns logs -l app.kubernetes.io/instance=hazelcast -f`


##### Reconfigure (enable `cpSubsystem`)
- `kubectl delete -f hazelcast-enterprise.yaml`
- add/remove the `cpSubsystem` block from the `*.yaml` manifest
- `kubectl apply -f hazelcast-enterprise.yaml`


##### Clean up
- `kubectl delete -f hazelcast.yaml`/`hazelcast-enterprise.yaml`
- `kubectl -n hazelcast-ns delete configmaps/hazelcast-config`
- `kubectl -n hazelcast-ns delete secrets/hazelcast-license-key` if `hazelcast-enterprise`
- `helm uninstall operator`
___
### Local
Launches 3 Docker containers locally in a shared network

1. Configure `hazelcast-config.yaml` if needed
   - switch `cp-subsystem` by setting `cp-member-count: 3` to enable/`cp-member-count: 0` to disable
2. `just start`/`sudo docker compose up -d`
3. `just logs`/`sudo docker compose logs -f`


## Run
Rename `tmp.env` to `.env`
- For the local setup, leave the `HZ_CLUSTER_MEMBERS` as is 

If you have `just` command runner:
- `just -l` - list all commands
- `just venv` - create a Python env and install dependencies
- `just help` - show the help for the script execution parameters
- `just start` - start the Docker service
- `just stop` - stop the Docker service
- `just logs` - show the Docker logs
- `just <method> <flags>` - run the counter with a specified method
- `just count-all <flags>` - run the counter with all methods in order
- `just count-no-cp <flags>` - run the counter with methods that don't use `cpSubsystem` structures

Without `just`:
- `ENV_NAME=<env_name>`
- `python3 -m venv $ENV_NAME`
- `source $ENV_NAME/bin/activate`
- `pip install -r requirements.txt`
- use `docker compose up`/`down`/`logs -f` to start/stop/logs the Docker service(s)
- replace `just` in the script execution commands by `python main.py --method`
- `python main.py --method <method> <flags>`

Specify `--connections <integer>` to set a number of simultaneous 'connections' (default is `10`)  
Specify `--iters <integer>` to set a number of increment request from each 'connection' (default is `10000`)


## Methods & results
#### The tests run in both, the cloud and local environment:
- `GCP GKE` - `3`x`e2-standart-4` with `8 vCPU`+`16GB RAM` each
- `docker compose` - `3` containers running on the host machine with `8 CPU`+`32GB RAM`

### `no locking` with `IMap`
**Read before write, increment on the client side, no write locks, causes a race condition**

`just count-imap-non-blocking`/`python main.py --method imap_non_blocking`

With the `--connections 10 --iters 10000` the result is in range `10000-20000`, nondeterministic  
`GKE`:
- local result `17037`
- time `~574 seconds`  
- time range between `1th` and `10th` connection `557-574 seconds`

`docker compose`:
- local result `18503`
- time `19.5 seconds`  
- time range between `1th` and `10th` connection `16.8-19.5 seconds`


### `pessimistic locking` with `IMap`
**Explicit write locks, locks until done, increment of the client side**

`just count-imap-pessimistic-lock`/`python main.py --method imap_pes_lock`

With the `--connections 10 --iters 10000` the result is `100000`  
`GKE`:
- time `~8388 seconds`  
- time range between `1th` and `10th` connection `8386-8388 seconds`

`docker compose`:
- time `83 seconds`  
- time range between `1th` and `10th` connection is milliseconds


### `optimistic locking` with `IMap`
**Without locks, before write compares the client and server values until they match**

`just count-imap-optimistic-lock`/`python main.py --method imap_opt_lock`

With the `--connections 10 --iters 10000` the result is `100000`  
`GKE`:
- time `3380 seconds`  
- time range between `1th` and `10th` connection `2474-3380 seconds`

`docker compose`:
- time `77.9 seconds`  
- time range between `1th` and `10th` connection `69.0-77.9 seconds`


### `CP Subsystem` with `IAtomicLong`
**Atomic structure intended to be a counter, works on top of the Raft consensus algorithm**

`just count-iatomiclong`/`python main.py --method iatomiclong`

With the `--connections 10 --iters 10000` the result is `100000`  
`GKE`:
- time `~320 seconds`  
- time range between `1th` and `10th` connection `300-320 seconds`

`docker compose`:
- time `9.6 seconds`  
- time range between `1th` and `10th` connection `8.1-9.6 seconds`