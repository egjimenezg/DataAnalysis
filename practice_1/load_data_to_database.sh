#!/bin/bash

#mv StatusData.csv StatusData1.csv

#python join_data.py
mysql -u root -p -e "SET GLOBAL local_infile='ON'";
mysql -u root -p -e "SOURCE database.sql";

mysql --local-infile=1 -u root -p -e "USE VEHICLES" -e "
  LOAD DATA LOCAL INFILE 'StatusDataComplete.csv'
  INTO TABLE STATUS_VEHICULO FIELDS TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n'
"
