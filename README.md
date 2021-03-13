# README
This repo contains the Dockerfile and relevant scripts for running BEAM and managing docker. <br />
Intended for: VIP AEGIS. <br />

## Build BEAM
Run the file docker/docker-build to build to docker image for BEAM.<br />
## Test BEAM
Run the file beam-test-run to test the beamville scenario.<br />
## MatSim Conversion
Several tools are provided.<br />
JOSM: latest tested jar is downloaded.<br />
MatSim: MatSim 12.0 release is downloaded.<br /> 
Osmosis: Osmosis 48.3 release is downloaded.<br />

JOSM is run through a GUI. A docker container is not necessarily needed to run JOSM since you just have to execute a jar file, but one is provided anyways.<br />
To run JOSM, launch the docker-open-JOSM-GUI script. If you are using Windows, you need to install VeXsrv Windows X Server. Then, launch the docker-open-JOSM-GUI-Windows script.<br />
JOSM's data can be saved to an external docker volume. Then, the data can be accessed in the docker volume with the export-JOSM-data script.<br />
The location of this volume is /JOSMVolume. Ensure that any data you want to save is saved to *THIS* folder or else the export script will not get any of your data.<br />


###### BEAM-related: <br />

beam-test-run: This script runs the gradle wrapper with the Beamville scenario and copies the output folder to host working directory.<br />
MatSimConversion/convert: This script converts the provided MatSim Scenario and related files to a BEAM Scenario


###### Docker-related:<br />
###### BEAM
docker/beam/Dockerfile: This is the docker build script that docker uses.<br />
docker/beam/docker-build: This script builds the docker image based on Dockerfile.<br />
docker/beam/docker-open-image: This script opens the docker image beam as a container for testing purposes.<br />

###### MatSim to BEAM conversion tools
docker/conversion-tools/Dockerfile: This is the docker build script that docker uses.<br />
docker/conversion-tools/Dockerfile-JOSM: This is the docker build script that docker uses.<br />
docker/conversion-tools/docker-build: This script builds the docker image based on Dockerfile.<br />
docker/conversion-tools/docker-open-image: This script opens the docker image beam as a container for testing purposes.<br />
docker/conversion-tools/docker-open-JOSM-GUI: This opens up JOSM's GUI and mounts the current external directory.<br />
docker/conversion-tools/docker-open-JOSM-GUI-Windows: This opens up JOSM's GUI and mounts the current external directory on Windows.<br />
docker/conversion-tools/export-JOSM-data: This exports data in the JOSMVolume Docker Volume

###### General
docker/remove-container: This script removes ALL docker containers. *USE WITH CAUTION*<br />
docker/purge-docker: This script removes ALL docker containers and ALL docker images. *USE WITH CAUTION*<br />
