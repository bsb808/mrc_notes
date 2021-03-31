

# Image: Build or Download?

## Download docker image

https://hub.docker.com/r/tfoote/test_novnc/tags?page=1&ordering=last_updated

```
docker pull tfoote/test_novnc:latest
```

## Build base docker image

This will get the Dockerfile from the git repo at https://github.com/tfoote/test_novnc and build it.

```
git clone git@github.com:tfoote/test_novnc.git
cd test_novnc
docker build -t test_novnc . 
```

Note: use the `test_novnc` tag rather than the `tfoote/test_novnc:latest` tag to distinguish between the locally built image and the image pulled from the remote repository. Only tag your local image to match the remote repository image if you intend to push the local image back to the repository (and replace the image that is already there). In this case, we don't want to do this (and we don't have permissions anyway).

## Create a Python virtual environemt and activate it

Create:
```
VENVPATH="${HOME}/novncrocker_venv"
mkdir -p ${VENVPATH}
python3 -m venv ${VENVPATH}
```
Activate:
```
cd ${VENVPATH}
. ${VENVPATH}/bin/activate
```
For any new terminal re activate the venv before trying to use it.

```
cd ${VENVPATH}
. ${VENVPATH}/bin/activate
```

## Install cuda-enabled rocker in the virtual environment
```
pip install git+https://github.com/osrf/rocker/pull/126
```

## Install novnc-rocker in the virtual environment
```
pip install git+https://github.com/tfoote/novnc-rocker.git
```

## Extend the base image with rocker 

This will use rocker to modify the local image built above and tagged with `test_novnc`
```
rocker --cuda --nvidia --novnc --turbovnc test_novnc
```
Use the above if the intent is to develop the docker image we built locally.

To run rocker on the image pulled from dockerhub, use:
```
rocker --cuda --nvidia --novnc --turbovnc tfoote/test_novnc:latest
```
Use this if you just want to run a local copy of the remote image and you either aren't planning on modifying it or you want to modify using the "commit" method.

## Run the rockerified image
* If rocker executes successfully, it will output the command you need to run it. 
* The command will looks something like this:
```
docker run --rm -it -p 8080:8080  --gpus all <image_hash>
```
* There is a small bug: you have to add an extra space in the command before `-p`.
* This bug prevents the machine from running automatically.
* I will submit an issue for it, but this is actually a little convenient (see below).
* Running this command manually should bring up the local novnc server.

### Recommended:
* Tag the image you just made so you can find it
```
docker tag novnc_local_rocker
```
* Now you can use this tag instead of the hash:
```
docker run --rm -it -p 8080:8080  --gpus all novnc_local_rocker
``` 

## Login via browser

Go to [http://localhost:8080/vnc.html](http://localhost:8080/vnc.html)

username and password are

`testuser:testpassword`

