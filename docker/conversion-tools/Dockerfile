FROM beam:latest
RUN apt install -y zip curl wget
RUN cd /home/beamuser && mkdir JOSM && cd JOSM && wget https://josm.openstreetmap.de/josm-tested.jar
RUN cd /home/beamuser && mkdir MatSim && cd MatSim && wget https://github.com/matsim-org/matsim-libs/releases/download/matsim-12.0/matsim-12.0-release.zip && unzip matsim-12.0-release.zip
RUN cd /home/beamuser && mkdir osmosis && cd osmosis && wget https://github.com/openstreetmap/osmosis/releases/download/0.48.3/osmosis-0.48.3.zip && unzip osmosis-0.48.3.zip
