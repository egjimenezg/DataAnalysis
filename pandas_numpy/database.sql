DROP DATABASE IF EXISTS VEHICLES;

CREATE DATABASE IF NOT EXISTS VEHICLES;

USE VEHICLES;

CREATE TABLE IF NOT EXISTS STATUS_VEHICULO(
  VEHICLE_TYPE VARCHAR(10),
  DATE_CREATED TIMESTAMP,
  DESCRIPTION VARCHAR(100),
  VALUE DECIMAL(20,10)
);