### picobytes-execute-test
## setup docker --- necessecary step
1. download docker desktop ------> https://www.docker.com/products/docker-desktop/
2. open docker desktop

# build docker image locally ---- for execute and test devs ---- public docker image steps below
1. at top level of repository, run command: 'docker build -t name_of_image .'

# make public docker image
1. modify docker build command as such: 'docker build -t docker_username/name_of_image:tag .'
            ex. 'docker build -t dewitt483/picobytes:v3 .'
2. push docker image: docker push docker_username/name_of_image:tag

# pull public docker image ---- best for picobytes core ---- the latest working version of a docker image will be made public
1. go to this link: https://hub.docker.com/r/dewitt483/picobytes/tags
2. copy the pull command from the desired image and run it on command line

# run docker container 
1. execute command: docker run -p localport:5000 image_name 


Now you can make calls into a single docker container

## setup kubernetes cluster

1. install kubernetes on your local machine, kubernetes and kubectl are required to execute cluster

# setup docker compatibility. 
1. go to docker desktop, then settings, then kubernetes
2. toggle the cluster on, select kubeadm, then click apply and restart

# deployment files setup
1. deployment files are .yaml files, there are 3 that need to be run
    a. pico-deployment.yaml sets up the image containers, within that file,     ensure all app fields are set to the same name, picobytes for example. Make sure the image field is set correctly to the picobytes container image
    b. in service.yaml file, make sure the external port is set to 5001, the name field can be whatever you want, and the app field needs to be the same as in pico-deployment.yaml
2. internal port should not be changed, but external port can be set to         whatever needed


# start the kubernetes cluster

1. run on command line: 'kubectl apply -f' followed by each yaml file
        ex. kubectl apply -f pico-deployment.yaml
    a. run 'kubectl get pods' to confirm containers are running
    b. run kubectl get services to confirm service is running
2. expose ports by running 
    kubectl port-forward service/name_field_in_service desiredport:5000 --address 0.0.0.0

Now you should have a cluster up and running that can be called the same way a single container is called. 







