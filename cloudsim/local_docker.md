

# Image: Build or Download?

## Download docker image

https://hub.docker.com/r/tfoote/test_novnc/tags?page=1&ordering=last_updated

```
docker pull tfoote/test_novnc:latest
```

## Build with script
* Get the `Dockerfile` and `build.bash` script from the git repo at https://github.com/tfoote/test_novnc. 

```
git clone git@github.com:tfoote/test_novnc.git
```
* Run the script `build.bash` script to generate and run a local `novnc` image.
```
cd test_novnc
bash build.bash
```
The script does the following:
* Builds the base image and names it `test_novnc`
* Creates and activates a python3 virtual environment called `test_novnc_venv` stored at `/tmp/test_novnc_venv`
* Installs the cuda-enabled branch of `rocker` and the main branch of `novnc-rocker`
* Calls `rocker` to inject layers for enabling support for cuda and nvidia, enables novnc and turbovnc, and turns on local user mode with the developer user. 

???: In the bash script it runs the image `test_novnc`.  I would have expected the image to be explicitly `test_novnc:latest`

## (TODO) How to add new features to the image

Following the instructions above generates a docker image tagged as `test_novnc:latest`.   Here we want to make incremental changes to the `Dockerfile` and rebuild an image, calling it `test_novnc:prototype` and then test the new features, while not modifying the `test_novnc:latest` so that we can work with both images - preseving access `test_novnc:latest` helps with reproducing what the students see.

1. Create a branch of https://github.com/tfoote/test_novnc
1. Make changes to Dockerfile
1. Rebuild from the Dockerfile `docker build . -t test_novnc:prototype`
1. Don't use the `build.bash` file, but instead start the container using a command such as...
```
IMAGE="test_novnc:prototype"
rocker --cuda --nvidia --novnc --turbovnc --user --user-override-name=developer ${IMAGE}
```



## Login via browser

Go to [http://localhost:8080/vnc.html](http://localhost:8080/vnc.html)

username and password are

`testuser:testpassword`

