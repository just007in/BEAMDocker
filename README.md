This repo contains the Dockerfile and relevant scripts for running BEAM and managing docker.
Intended for: VIP AEGIS

BEAM-related:

docker-build: This script builds the docker image based on Dockerfile
docker-test-run: This script runs the gradle wrapper with the Beamville scenario and copies the output folder to host working directory


Docker-related:

Dockerfile: This is the docker build script that docker uses
docker-open-image: This script opens the docker image beam as a container for testing purposes
remove-container: This script removes ALL docker containers. USE WITH CAUTION
purge-docker: This script removes ALL docker containers and ALL docker images. USE WITH CAUTION
