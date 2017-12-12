#!/bin/bash

set -xe

echo "-----------hello vios------------"
python /vios/VIOS/manage.py migrate 
python /vios/VIOS/manage.py runserver 0.0.0.0:8000
