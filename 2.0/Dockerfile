FROM ubuntu:17.10
LABEL version="1.0" description="virus identification on site" maintainer="Su YaNan <suyanan1991@163.com>"

COPY ./requirements.txt /vios/requirements.txt

RUN set -xe \
  && apt update \
  && apt install -y \
    build-essential \
    openjdk-8-jdk \
    python-pip \
    python-tk \
    libmysqlclient-dev \
  && pip install --upgrade pip \
  && pip install -r /vios/requirements.txt \
  && apt install -y \
    trimmomatic \
    bowtie2 \
    ncbi-blast+ \
  && rm -rf /var/lib/apt/lists/

WORKDIR /vios/softwares
COPY ./softwares /vios/softwares

RUN tar -zxf velvet_1.2.10.tgz \
  && rm velvet_1.2.10.tgz \
  && cd velvet_1.2.10 \
  && make 'CATEGORIES=10' 'MAXKMERLENGTH=127' 'BIGASSEMBLY=1' 'LONGSEQUENCES=1' 'OPENMP=1' 'BUNDLEDZLIB=1' \
  && cd ../

# environment variables
ENV SOFTWARE_HOME=/vios/softwares
ENV TRIMMOMATIC_HOME=/usr/share/java VELVET_HOME=$SOFTWARE_HOME/velvet_1.2.10
ENV PATH=$TRIMMOMATIC_HOME/trimmomatic.jar:$VELVET_HOME:$PATH

WORKDIR /vios/VIOS

# volumn by 'docker run'
VOLUME /vios/VIOS
VOLUME /vios/database

ENV VIOS_HOME=/vios/VIOS
ENV DATABASE_HOME=/vios/database

COPY ./run.sh /vios/run.sh

EXPOSE 8000
CMD ["/bin/sh","/vios/run.sh"]
