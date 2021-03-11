# README
This repo contains the Dockerfile and relevant scripts for running BEAM and managing docker. <br />
Intended for: VIP AEGIS. <br />

## Build BEAM
Run the file docker/docker-build to build to docker image for BEAM.<br />
## Test BEAM
Run the file beam-test-run to test the beamville scenario.<br />

###### BEAM-related: <br />

beam-test-run: This script runs the gradle wrapper with the Beamville scenario and copies the output folder to host working directory.<br />


###### Docker-related:<br />

docker/Dockerfile: This is the docker build script that docker uses.<br />
docker/docker-build: This script builds the docker image based on Dockerfile.<br />
docker/docker-open-image: This script opens the docker image beam as a container for testing purposes.<br />
docker/remove-container: This script removes ALL docker containers. *USE WITH CAUTION*<br />
docker/purge-docker: This script removes ALL docker containers and ALL docker images. *USE WITH CAUTION*<br />
