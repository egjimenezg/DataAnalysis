#!/bin/bash

#python join_data.py

mysql --local-infile=1 -u root -p -e "SET GLOBAL local_infile='ON';" -e "SOURCE database.sql;" \
-e "USE VEHICLES;" \
-e "LOAD DATA LOCAL INFILE 'StatusDataComplete.csv'
    INTO TABLE STATUS_VEHICULO FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n'"

