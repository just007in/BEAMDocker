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
MatSim to BEAM conversion tool: Included with BEAM installation.<br />

Other helpful tools: osmconvert to convert a .osm to .osm.pbf file.<br />

### Steps to Convert a MatSim scenario to a basic BEAM scenario
Step 4 is if the more advanced parameters and files were not created specifically for BEAM.<br />
These files would not be generated since information in these files are not in the MatSim Scenario.<br />

1. Create a folder with the name of your scenario. Case-Sensitive.
2. Copy and paste your BEAM scenario configuration, population.xml file, network.xml file, and .osm.pbf file.
3. In the directory containing your scenario folder, run the script MatSimConversion/convert with the first argument as the scenario name.
4. Copy/Create/Modify files that are also needed. The convert script should output the names of the missing files. 
    1. You most likely have to modify vehicleTypes.csv to include additional column data and the BODY-TYPE-DEFAULT vehicle. Take a look at MatSimConversion/vehicleTypes.csv for an example of a correctly formatted vehicleTypes.csv file.
    2. Extract households.xml.gz and population.xml.gz 

### MatSim Conversion Considerations
<details> <summary>Changes to the provided MatSimConversion/skeleton.conf file</summary>
<p>The provided skeleton.conf file had changes to create a very basic BEAM scenario.</p> 
**Mode Choice Algorithm**
<p>
beam.agentsim.agents.modalBehaviors.modeChoiceClass was set to "ModeChoiceDriveIfAvailable"<br />
According to the documentation, the beam.agentsim.agents.modalBehaviors.lccm.filePath should be ignored but just to be safe, this parameter was removed.
</p>
**Other Removed Parameters** <br />
- beam.agentsim.agents.modeIncentive.filePath<br />
- beam.agentsim.agents.ptFare.filePath <br />
- beam.agentsim.agents.vehicles.linkToGradePercentFilePath <br />
- beam.agentsim.toll.filePath <br />
- beam.agentsim.taz.filePath <br />
- beam.agentsim.taz.parkingFilePath <br />

**RideHail Fleet** <br />
<p>
- beam.agentsim.agents.rideHail.initialization.initType was set to “FILE”.
    This requires beam.agentsim.agents.rideHail.initialization.filePath to be valid. The filename is rideHailFleet.csv. This can be set to a table with no entries. <br />

- beam.agentsim.agents.rideHail.initialization.procedural.vehicleTypeId was set to “CAR”<br />
- beam.agentsim.agents.rideHail.initialization.procedural.fractionOfInitialVehicleFleet was set to 0.0
</p>
**Beam Spatial**
<p>
- The localCRS in beam.spatial was set to epsg:3857<br />

- Beam.routing r5 mNetBuilder.toCRS was set to ${beam.spatial.localCRS} 
</p>
**Shapefile**
<p>A shapefile using the matsim.conversion.shapeConfig.shapeFile parameter was not specified. The matsim.conversion.shapeConfig.tazIdFieldName was not specified.</p>

**Benchmark file**
<p>The benchmark file was set so only driving cars was set. This was done by setting everything to 0 except for cars. Not sure why this is required.</p>

**Vehicle Types** <br />
Since the MatSim conversion program outputs vehicle types with missing columns, a python script using pandas was used to add the necessary columns to the csv file. A program like Excel can also be used. <br />
The additional columns include:<br />
- primaryVehicleEnergyFile<br />
- secondaryVehicleEnergyFile<br />
- monetaryCostPerMeter<br />
- monetaryCostPerSecond<br />
- sampleProbabilityWithinCategory<br />
- chargingCapability<br />
The vehicleCategory column was modified. Passenger vehicles were set to Car. Public transportation vehicles are set to MediumDutyPassenger. A person walking is set to Body.<br />

The row for the vehicle body type was also added.<br />

**Time Zones**
<p>
According to the program: BEAM uses the R5 router, which was designed as a stand-alone service either for doing accessibility analysis or as a point to point trip planner. R5 was designed with public transit at the top of the developers? minds, so they infer the time zone of the region being modeled from the 'timezone' field in the 'agency.txt' file in the first GTFS data archive that is parsed during the network building process.<br />

Therefore, if no GTFS data is provided to R5, it cannot infer the locate timezone and it then assumes UTC.<br />

If no GTFS data for transit agencies is provided to R5, set the baseDate in beam.routing to have an offset of 00:00. Example: "2016-10-17T00:00:00-00:00"<br />
</p>
</details>

### JOSM
JOSM is run through a GUI. A docker container is not necessarily needed to run JOSM since you just have to execute a jar file, but one is provided anyways.<br />
To run JOSM, launch the docker-open-JOSM-GUI script. If you are using Windows, you need to install VeXsrv Windows X Server. Then, launch the docker-open-JOSM-GUI-Windows script.<br />
JOSM's data can be saved to an external docker volume. Then, the data can be accessed in the docker volume with the export-JOSM-data script.<br />
The location of this volume is /JOSMVolume. Ensure that any data you want to save is saved to *THIS* folder or else the export script will not get any of your data.<br />
The export script moves the contents of /JOSMVolume to the folder JOSM in your current working directory. *NOTE* That the files are *NOT* copied but moved. <br />

## Overview of Most Files
##### BEAM-related: <br />

beam-test-run: This script runs the gradle wrapper with the Beamville scenario and copies the output folder to host working directory.<br />
beam-run-scenario: This script runs the provided scenario in test/input/[scenario-name]. The name of the scenario must be provided to the script.<br />
MatSimConversion/convert: This script converts the provided MatSim Scenario and related files to a BEAM Scenario.<br />
MatSimConversion/skeleton.conf: This is a sample BEAM configuration file with some parameters commented out. The scenario name is skeleton.<br />

##### MatSim to Beam Conversion related: <br />
MatSimConversion/convert: This script does a rudimentary conversion using the MatSim to BEAM scenario converter tool provided by BEAM.<br />
MatSimConversion/genpopulation.py: This script does a basic generation of a MatSim population.xml (plans.xml) file for a MatSim scenario.<br />
MatSimConversion/vehicleTypes.csv: This file contains the correct format for a vehicleTypes file for a BEAM scenario.<br />

##### Docker-related:<br />
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

##### General
docker/remove-container: This script removes ALL docker containers. *USE WITH CAUTION*<br />
docker/purge-docker: This script removes ALL docker containers and ALL docker images. *USE WITH CAUTION*<br />
