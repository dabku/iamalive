# iamalive [![Build Status](https://travis-ci.org/dabku/iamalive.svg?branch=master)](https://travis-ci.org/dabku/iamalive)

![](docs/img/front.PNG)

## Summary
Simple tool to monitor scripts/components of the various devices I am running. 
Created with intention of deploying it on multiple 
[ESP8266](https://docs.micropython.org/en/latest/esp8266/quickref.html) running [MicroPython](https://micropython.org/).

## Technologies

- Flask Restful
- MongoDB
- Angular8

## Run demo

- clone repository
- install docker
- run ``docker-compose up``
- type in 127.0.0.1 in your web browser

[Client Example](client_example/client_example.py) is available to go through the whole process of adding new device
and updating it's properties.

## Frontend

Frontend was made in Angular8 with no prior experience in this framework,
keep that in mind if you wish to use parts of the code.

- Services to
    - Periodically check the connection to the API
    - Handle the retrieval of the devices
    - Handle the  authorization
- Interceptors to handle 
    - setting the correct API url
    - de-authorize on 401 error code
    - add authentication headers
- Route guard for automatic redirection to the login page

## Backend

Backend is developed in Flask-Restful framework interacting with NongoDB. 
MongoDB was choosen as project has dictionary-like structure with dynamic structure.


## Todo

List of the items that may be needed in the future

- JWT (when available in micro python)
- Historical logs (Maybe [InfluxDB](https://www.influxdata.com/products/influxdb-overview/))
- Notifications (re-use [my Discord bot](https://github.com/dabku/FeedPi/blob/master/libs/discordbot.py) or emails )
- Edit/delete- full data management from frontend
- Allow devices to check status/properties of all the other devices
- Run API on proper server, probably nginx
