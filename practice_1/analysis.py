import pandas as pd
import sqlalchemy
import numpy as np

from numpy import arange, array, ones, linalg
from pylab import plot, show

engine = sqlalchemy.create_engine("mysql+pymysql://root:n0m3l0s3@localhost:3306/VEHICLES")

df = pd.read_sql_table("STATUS_VEHICULO",engine,columns=['VEHICLE_TYPE','DATE_CREATED','DESCRIPTION','VALUE'])

df['YEAR'] = df['DATE_CREATED'].dt.year
df['MONTH'] = df['DATE_CREATED'].dt.month
df['DAY'] = df['DATE_CREATED'].dt.day

vehicles_data = df.groupby(['VEHICLE_TYPE','YEAR','MONTH','DAY']).apply(lambda x: pd.Series(dict(
  max_fuel=(x.loc[x.DESCRIPTION == "DiagnosticTotalFuelUsedId"].VALUE.max()),
  min_fuel=(x.loc[x.DESCRIPTION == "DiagnosticTotalFuelUsedId"].VALUE.min()),
  max_distance = (x.loc[x.DESCRIPTION == 'DiagnosticOdometerId'].VALUE.max()),
  min_distance = (x.loc[x.DESCRIPTION == 'DiagnosticOdometerId'].VALUE.min())
))).reset_index()

vehicles_data['distance'] =  vehicles_data['max_distance']-vehicles_data['min_distance']
vehicles_data['fuel'] = vehicles_data['max_fuel']-vehicles_data['min_fuel']

dirty_data = vehicles_data[pd.isna(vehicles_data['fuel']) | pd.isna(vehicles_data['distance']) |
                           (vehicles_data['distance'] == 0 | pd.isna(vehicles_data['distance'])) |
                           (vehicles_data['fuel'] == 0 | pd.isna(vehicles_data['distance'])) ]

vehicles_data = vehicles_data[pd.notnull(vehicles_data['max_fuel']) & pd.notnull(vehicles_data['max_distance'])]
vehicles_data = vehicles_data[vehicles_data['distance'] > 0]
vehicles_data = vehicles_data[vehicles_data['fuel'] > 0]

y = vehicles_data['distance']
xi = vehicles_data['fuel']

A = array([xi, ones(len(xi))])

w = linalg.lstsq(A.T,y)[0]

#y = mx+b
line = (w[0]*xi+w[1])
plot(xi,line,'r-',xi,y,'o')
show()


