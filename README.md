# VIOS
Virus Identification On Site

[TOC]

### INTRODUCTION

    **1.0/directory** includes some ngs softwares, supported with ubuntu16.04. *The image is too fat ,so not recommended.*；

    **2.0/derectory** is through ubuntu17.10 repository list including some ngs softwares. *The image is so simple , so recommended.*；

    VIOS function is to identify **virus** and confirm its classitication.
    From ngs **FASTQ** data, VIOS can achieve that the viruses category 、proportion 、coverage , and so on.

## method1：link(useful, not recommend)
1. set *DATABASE* variable in *settings.py*:
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vios_db',
            'HOST':'mysqler',  #mysql_container_hostname(--hostname=mysqler)
            'PORT':'3306',
            'USER':'root',
            'PASSWORD':'1234aaaa',
        }
    }
    ```
2. start *myslq* container, and appoint the *hostname* para same with the *HOST* element of *DATABASE* variable:
    ```
    docker run -it --hostname=mysqler --name mysql -e MYSQL_ROOT_PASSWORD=1234aaaa -e MYSQL_DATABASE=vios_db mysql:5.7
    ```
3. start *vios* container, and appoint the *link* para which can connect to MySQL:
    create image, first：
    > docker image build -t suyanan/vios:1.0 .
    > docker pull suyanan/vios:1.0

    ```
    docker container run -it --name vios --hostname vioser -v `pwd`/VIOS:/vios/VIOS -v `pwd`/database:/vios/database --link mysql:db suyanan/vios:1.0
    docker inspect -f '{{.NetworkSettings.IPAddress}}' vios
    #add IP manually, IF IP is not included int *ALLOWED_HOSTS* variable.
    ALLOWED_HOSTS = [
    u'127.0.0.1',
    u'localhost',
    u'172.17.0.3',
    ]
    ```
    FIANLLY, access *IP:8000* in browser.

    **CAUTION**：

      *link* para is useful but not recommended in current Docker version(1.17).


## method2 : network（useful, recommed）
1. generate network
    ```
    docker network create neter
    ```
2. start *mysql* container, and appoint the network
    ```
    docker run -it --hostname=mysqler --network neter --name mysql -e MYSQL_ROOT_PASSWORD=1234aaaa -e MYSQL_DATABASE=vios_db mysql:5.7
    ```
3. start *vios* container，and make its network same with that of *mysql* container(both network is **neter**)，achieve the access to MySQL
    create image, first：
    > docker image build -t suyanan/vios:1.0 .
    > docker pull suyanan/vios:1.0

    ```
    docker container run -it --name vios --hostname vioser --network neter -v `pwd`/VIOS:/vios/VIOS -v `pwd`/database:/vios/database suyanan/vios:1.0
    ```
    ```
    docker inspect mysql
    docker inspect vios
    ```
4. set the *HOST* elemen of *DATABASE* variable and *ALLOWED_HOSTS* variable in *settings.py*:
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vios_db',
            'HOST': ##mysql_container_ip
            'PORT':'3306',
            'USER':'root',
            'PASSWORD':'1234aaaa',
        }
    }
    ALLOWED_HOSTS = [
    u'127.0.0.1',
    u'localhost',
    #vios_container_ip
    ]
    ```

    **CAUTION**：

      - Just RESTART the *vios* container if you can't find *sample_list* or *sample_se_list* AFTER you upload your raw FASTQ datas.
      - start container with two commands:
        ```
        dockecontainer run -it --name vios --hostname vioser --network neter -v `pwd`/VIOS:/vios/VIOS -v `pwd`/database:/vios/database vios_pipeliner sh -c "python /vios/VIOS/manage.py migrate && python /vios/VIOS/manage.py runserver 0.0.0.0:8000"
        ```
      - start container with */bin/bash* to test internally(cover the *CMD* in Dockerfile):
        ```
        dockecontainer run -it --name vios --hostname vioser --network neter -v `pwd`/VIOS:/vios/VIOS -v `pwd`/database:/vios/database vios_pipeliner /bin/bash
        ```


## method3 : compose manages the two containers（optimal, at present）

    ```
    docker tag suyanan/vios：1.0 vioser_pipeliner
    OR:
    docker-compose up  #create and start containers
    docker-compose down -v   #shutdown and remove containers
    ```

    **CAUTION**：
      - There are still problems with using compose to manage the two containers(pipelinre——same as vios, and mysql)：
        *pipeliner_1  | django.db.utils.OperationalError: (2003, "Can't connect to MySQL server on 'mysqler' (111)")*

---

## CAUTION!!!：

1. local images：
    ```
    docker image save suyanan/vios:x.0 -o suyanan_vios_x.0.tar
    docker image load -i suyanan_vios_x.tar
    ```
2. warning messages while building Dckerfile：
    > WARNING: apt does not have a stable CLI interface. Use with caution in scripts.
    > debconf: delaying package configuration, since apt-utils is not installe

3. NO supporting window interface WITH Docker deployment
    SO：Force matplotlib to not use any Xwindows backend.
    add codes below in file *config_para.py*：
    ```
    import matplotlib
    matplotlib.use('Agg')
    ```
    The visualization results is located in corresponding directories.

4. softwares downloaded postion：

    **1.0/directory** : JAVA and ngs softwares is necessary，and you can download from [BaiduYun](https://pan.baidu.com/s/1sln1FcD);

    **2.0/directory** : [velvet](https://packages.ubuntu.com/artful/science/velvet) is necessary，but you need to decompress and rename with "velvet_1.2.10.tgz", and recompress it.
<br>
---
**COPY RIGHT**

201712.11

The End
