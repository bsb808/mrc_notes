

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

## Login via browser

Go to [http://localhost:8080/vnc.html](http://localhost:8080/vnc.html)

username and password are

`testuser:testpassword`

