# build COMMAND : docker image build -t suyanan/vios:1.0 .
# run mysql COMMAND : docker run -it --hostname=mysqler --name mysql -e MYSQL_ROOT_PASSWORD=1234aaaa -e MYSQL_DATABASE=vios_db mysql:5.7
# run vios COMMADN : docker container run -it --name vios --hostname vioser -v `pwd`/VIOS:/vios/VIOS -v `pwd`/database:/vios/database --link mysql:db suyanan/vios:1.0
# default : /bin/sh run.sh

FROM ubuntu:16.04

# author
LABEL version="1.0" description="virus identification on site" maintainer="Su YaNan <suyanan1991@163.com>"

COPY . /vios/

# ----basic operations pre-requirement----
RUN apt -y update \
&& apt install -y build-essential autoconf zlib1g zlib1g.dev zip vim python-pip python-tk libmysqlclient-dev
RUN pip install --upgrade pip && pip install -r /vios/requirements.txt


####
WORKDIR /vios/softwares
ENV SOFTWARE_HOME=/vios/softwares

# ----java----
RUN tar -zxvf jdk-8u131-linux-x64.tar.gz \
&& rm jdk-8u131-linux-x64.tar.gz
ENV JAVA_HOME=$SOFTWARE_HOME/jdk1.8.0_131
ENV CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV PATH=$JAVA_HOME/bin:$PATH

# ----Bioinformatics softwares:QC/map&alignment/assembly----
RUN unzip Trimmomatic-0.36.zip \  
&& rm Trimmomatic-0.36.zip \
&& unzip bowtie2-2.2.9-source.zip \ 
&& rm bowtie2-2.2.9-source.zip bwa-0.7.12.tar.bz2 \
&& cd bowtie2-2.2.9 \
&& make \
&& cd ../ \
&& tar -zxvf ncbi-blast-2.4.0+x64-linux.tar.gz \
&& rm ncbi-blast-2.4.0+x64-linux.tar.gz \
&& tar -zxf velvet_1.2.10.tgz \  
&& rm velvet_1.2.10.tgz \
&& cd velvet_1.2.10 \
&& make 'CATEGORIES=10' 'MAXKMERLENGTH=127' 'BIGASSEMBLY=1' 'LONGSEQUENCES=1' 'OPENMP=1' 'BUNDLEDZLIB=1' \
&& cd ../ 

# environment variables
ENV TRIMMOMATIC_HOME=$SOFTWARE_HOME/Trimmomatic-0.36 BOWTIE2_HOME=$SOFTWARE_HOME/bowtie2-2.2.9 BLAST_HOME=$SOFTWARE_HOME/ncbi-blast-2.4.0+ VELVET_HOME=$SOFTWARE_HOME/velvet_1.2.10
ENV PATH=$TRIMMOMATIC_HOME/trimmomatic-0.36.jar:$BOWTIE2_HOME:$BLAST_HOME/bin:$VELVET_HOME:$PATH

WORKDIR /vios/VIOS

# volumn by 'docker run'
VOLUME /vios/VIOS
VOLUME /vios/database

ENV VIOS_HOME=/vios/VIOS
ENV DATABASE_HOME=/vios/database

EXPOSE 8000
CMD ["/bin/sh","/vios/run.sh"]
