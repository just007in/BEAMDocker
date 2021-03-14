FROM amd64/ubuntu:latest
RUN apt update && apt upgrade -y

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt install -y sudo nano vim git git-lfs openjdk-8-jdk
RUN apt install -y python3 python3-pip python3-rtree libproj-dev proj-data proj-bin libgeos-dev npm
RUN pip3 install --upgrade setuptools
RUN pip3 install numpy pandas cython sklearn matplotlib mapclassify descartes geopandas contextily plotly collections-extended psutil requests
RUN useradd -m -p beam -s /bin/bash beamuser
RUN usermod -aG sudo beamuser

RUN cd /home/beamuser && git clone https://github.com/LBNL-UCB-STI/beam.git && cd beam && export MAXRAM=10g && ./gradlew :run -PappArgs="['--config', 'test/input/beamville/beam.conf']"


