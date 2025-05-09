### picobytes-execute-test
A scalable execution and testing backend for source code, running in Docker or Kubernetes. Designed to compile, execute, and validate code with sandboxing and memory analysis via Valgrind.

## Table of Contents

1. [Overview](#picobytes-execute-test)
2. [Technologies](#technologies-used)
3. [Features](#features)

### Docker Usage
4. [Install Docker](#setup-docker---necessecary-step)
5. [Build Docker Image Locally](#build-docker-image-locally----for-execute-and-test-devs----public-docker-image-steps-below)
6. [Publish Docker Image](#make-public-docker-image)
7. [Pull Public Docker Image](#pull-public-docker-image----best-for-picobytes-core----the-latest-working-version-of-a-docker-image-will-be-made-public)
8. [Run Docker Container (Monolithic Mode)](#run-docker-container-monolithic-mode----this-will-only-work-if-using-the-version-with-api-and-compiling-in-one-container)

### Kubernetes Setup
9. [Install Kubernetes](#setup-kubernetes-cluster)
10. [Configure Deployment Files](#deployment-files-setup)
11. [Start the Kubernetes Cluster](#start-the-kubernetes-cluster----if-not-already-started-by-constructpy)

### API Usage
12. [Sending Requests](#sending-requests-into-cluster-or-container)
13. [Input Schema](#input-schema)
14. [Output Schema](#output-schema)
### Worker Logs
15. [Worker Logging](#worker-logs)
### Operational Support
16. [Troubleshooting](#troubleshooting)
17. [Security Considerations](#security-considerations)

## Technologies used

- [Docker](https://www.docker.com/)
- [Kubernetes](https://kubernetes.io/)
- [Redis](https://redis.io/)
- [FASTAPI](https://github.com/tiangolo/fastapi)
- [Valgrind](https://valgrind.org/)
- [Python](https://www.python.org/)
- [Bash](https://www.gnu.org/software/bash/)

## Features
- Isolated environment for running user submitted code
- Compiling, executing and testing user submitted code
- Valgrind analysis
- API to communicate with our service
- Customizable options in the api on how the code should run. Examples: custom time limits, custom tests, whether to run the tests or not
- Blacklisting functions: functions that are not allowed to be used in the code
- Whitelisted functions: only functions that can be used in the code
- Resource limiting: amount of memory program can use, network access, time limits
- Timing how long each step such as : compilations, execution took
- Parsing the output to return a line by line analysis on the code
- Parsing the valgrind output to be more readable by the user
- Decoupling the API and computation allowing us to scale each part independently depending on the request load and load type
- Autoscaling of resources based on the workload
- Return a list of tests that failed
- Automatic recovery in case any components fail
- Clean up after each job is completed
- Persistant logging even if worker crashes

## Setup docker --- necessecary step
1. download docker ------> https://docs.docker.com/get-started/

## Build docker image locally ---- for execute and test devs ---- public docker image steps below
1. at top level of repository, run `construct.py` in order to build the images and start the kubernetes node described in the 'kubernetes-setup' folder
2. if this doesn't work try running the commands `docker build -t picobytes:api ./api` and `docker build -t picobytes:compile ./compile`

## Make public docker image
1. modify docker build command as such: `docker build -t docker_username/name_of_image:tag .`
ex. `docker build -t dewitt483/picobytes:v3 .`
2. push docker image: `docker push docker_username/name_of_image:tag`

## Pull public docker image ---- best for picobytes core ---- the latest working version of a docker image will be made public
1. go to this link: https://hub.docker.com/r/dewitt483/picobytes/tags
2. Link to the latest docker image [unstable]: https://hub.docker.com/r/na0maly/picobytes-execute-test
3. copy the pull command from the desired image and run it on command line

## Run docker container (monolithic mode) --- this will only work if using the version with api and compiling in one container
execute command: `docker run -p localport:5000 image_name` 


Now you can make calls into a single docker container

## Setup kubernetes cluster

1. install kubernetes on your local machine, kubernetes and kubectl are required to execute cluster ------> https://kubernetes.io/

## Deployment files setup
- deployment files are .yaml files, they are located in the /kubernetes-setup/ folder
- pico-deployment.yaml sets up the API container(s), within that file, ensure all app fields are set to the same name, picobytes for example. Make sure the image field is set correctly to the picobytes:api container image
- in service.yaml file, make sure the internal port is set to the same as the pikubeytes app configured in pico-deployment.yaml. The external port can be changed to whatever is available on your system
- redis-deployment and redis-service can have their ports changed but the server_api.py and worker.py need to be updated to reflect the new port or else they will not connect.
- worker-deployment configures the compile containers, limits can be set here for both the compiling container itself and its sidecar logging container
- components configures the metrics server that allows for autoscaling. Generally don't change this.
- autoscale configures the horizontal autoscaling of worker pods, min and max can be changed here along with targeted utilization of resources


## Start the kubernetes cluster -- if not already started by `construct.py`

1. run on command line: `kubectl apply -f ./kubernetes-setup`
- run `kubectl get pods` to confirm containers are running
- run `kubectl get services` to confirm service is running
2. expose ports (if not already) by running 
- `kubectl port-forward service/name_field_in_service desiredport:5000 --address 0.0.0.0`

Now you should have a cluster up and running that can be called the same way a single container is called.


## Sending requests into cluster or container

1. if configured properly JSON requests can be sent into host_ip:5000/submit

Input Schema
-------------
code: string  
&nbsp;&nbsp;&nbsp;&nbsp;**Required.** The source code to execute. Do not define main() in this, use a different name

tests: string | null  
&nbsp;&nbsp;&nbsp;&nbsp;Optional. Test cases to run against the code. Format of `assert(func(x)==y)`

timeout: integer (default: 15)  
&nbsp;&nbsp;&nbsp;&nbsp;Optional. Maximum total execution time in seconds.

perTestTimeout: integer (default: 5)  
&nbsp;&nbsp;&nbsp;&nbsp;Optional. Time limit per test case in seconds.

whitelisted: list of strings | null  
&nbsp;&nbsp;&nbsp;&nbsp;Optional. List of functions or imports explicitly allowed. Must allow function names defined in code.

blacklisted: list of strings | null  
&nbsp;&nbsp;&nbsp;&nbsp;Optional. List of functions or imports explicitly forbidden.


Output Schema
-------------
build: boolean  
&nbsp;&nbsp;&nbsp;&nbsp;True if the code built successfully (e.g., compilation step passed).

compile: boolean  
&nbsp;&nbsp;&nbsp;&nbsp;True if the compilation process itself succeeded without errors.

run: boolean  
&nbsp;&nbsp;&nbsp;&nbsp;True if the code executed without crashing or timing out.

output: string  
&nbsp;&nbsp;&nbsp;&nbsp;The combined standard output and messages from execution.

compilation_time: float  
&nbsp;&nbsp;&nbsp;&nbsp;Time in seconds taken to compile the code.

run_time: float  
&nbsp;&nbsp;&nbsp;&nbsp;Time in seconds taken to execute the compiled code.

valgrind: string  
&nbsp;&nbsp;&nbsp;&nbsp;Parsed Valgrind output giving information on memory leaks

formatted_response: list  
&nbsp;&nbsp;&nbsp;&nbsp;List of errors that occured inside submitted code with the line number inside the code. May be empty.

failed_tests: list  
&nbsp;&nbsp;&nbsp;&nbsp;List of numbers that correspond to tests that failed, if any.

## Worker Logs
- Worker logs of individual pods can be accessed by finding available pods through `kubectl get pods` and doing the following: `kubectl logs pod_name -c fluent-bit`

## Troubleshooting

- `connection refused`: Confirm port-forwarding is active via `kubectl port-forward`.
- `redis connection error`: Check that the Redis pod is running with `kubectl get pods`.
- `ImagePullBackOff`: Ensure the image name in the deployment YAML matches an existing public or locally built image.

## Security Considerations

- Currently these containers are NOT hardened beyond switching off root user. PLEASE take appropriate measures to ensure they are properly secured with read-only root and disabled network capabilities
- Code is run in isolated containers with timeouts and optional function blacklisting.






