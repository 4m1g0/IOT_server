Web services for IOT project
===========================================

This repository contains the services to support the IOT project.
See the NOTICE to view the full list of dependencies.

This repository is part of a larger project designed to minimize costs using hourly prices of the energy and a set of scheduling algorithms.

You can visit the other modules here
 - Web Application (https://github.com/4m1g0/angular_ui)
 - Firmware (https://github.com/4m1g0/IOT_tfg)

### List of services ###
 - Pricing Service. Is located between REE (http://www.ree.es/es/) API and provides hourly prices.
 - API Server. Exposes a API REST so that any application can use it-
 - IOT Server. Is a proxy server which stores persistent conections from the nodes

### Docker ###
All this services are deployed using docker. An updated version of the Docker imageiks abailable here: https://hub.docker.com/r/4m1g0/auto_iot_server/

It can be run ussing:
docker run -it -p 8080:8080 -p 8081:8081 -p 9000:9000 -p 9001:9001 4m1g0/auto_iot_server
