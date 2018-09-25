#!/bin/bash

#mv StatusData.csv StatusData1.csv

#python join_data.py

mysql -u root -e "SOURCE database.sql"

mysql -u root -e "USE VEHICLES" -e "
  LOAD DATA LOCAL INFILE 'StatusDataComplete.csv'
  INTO TABLE VEHICLES FIELDS TERMINATED BY ','
  OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n'
"
