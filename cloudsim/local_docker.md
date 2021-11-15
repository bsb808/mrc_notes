
# Dependencies

```
sudo apt update
sudo apt install nvidia-docker2
sudo systemctl restart docker
```

# Image: Build or Download?

## Download docker image

https://hub.docker.com/r/tfoote/test_novnc/tags?page=1&ordering=last_updated

```
docker pull tfoote/test_novnc:latest
```

```
docker run --rm -it -p 8080:8080 --gpus all tfoote/test_novnc:main

```
OR
```
docker pull learninglab/me4823:matlab_small
docker run --rm -it -p 8080:8080 --gpus all learninglab/me4823:matlab_small
```


https://hub.docker.com/u/learninglab

## Build with docker image 

Get the `Dockerfile` and from the git repo at https://github.com/tfoote/test_novnc. 

```
git clone git@github.com:tfoote/test_novnc.git
```

Build the image and tag it specifically as a tag that differentiates it from the downloaded image.  
```
docker build --tag test_novnc:local_latest ./
```

## Run a local image


If not done previously, setup a virtual env

```
mkdir -p /tmp/test_novnc_venv
python3 -m venv /tmp/test_novnc_venv
```

Activate and install wheel, the cuda-enabled branch of `rocker` and the main branch of `novnc-rocker`
```
. /tmp/test_novnc_venv/bin/activate
pip install wheel
pip install -U git+https://github.com/osrf/rocker.git@cuda
pip install -U git+https://github.com/tfoote/novnc-rocker.git@main
```

Specify the desired image and run with rocker

```
IMAGE="test_novnc:local_latest"
rocker --cuda --nvidia --novnc --turbovnc --user --user-override-name=developer ${IMAGE}
```&


Finally open the UI in a browser: [http://localhost:8080/vnc.html](http://localhost:8080/vnc.html)

username and password are

`testuser:testpassword`

## How to add new features to the image

Following the instructions above generates a docker image tagged as `test_novnc:local_latest`.   Here we want to make incremental changes to the `Dockerfile` and rebuild an image, calling it `test_novnc:local_prototype` and then test the new features, while not modifying the `test_novnc:local_latest` so that we can work with both images - preseving access `test_novnc:local_latest` helps with reproducing what the students see.

1. Create a branch of https://github.com/tfoote/test_novnc
1. Make changes to Dockerfile
1. Rebuild from the Dockerfile `docker build . -t test_novnc:local_prototype`
1. Test the image locally
1. Push a PR
