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
df['WEEK'] = df['DATE_CREATED'].dt.week

vehicles_data = df.groupby(['VEHICLE_TYPE','YEAR','MONTH','DAY','WEEK']).apply(lambda x: pd.Series(dict(
  max_fuel=(x.loc[x.DESCRIPTION == "DiagnosticTotalFuelUsedId"].VALUE.max()),
  min_fuel=(x.loc[x.DESCRIPTION == "DiagnosticTotalFuelUsedId"].VALUE.min()),
  max_distance = (x.loc[x.DESCRIPTION == 'DiagnosticOdometerId'].VALUE.max()),
  min_distance = (x.loc[x.DESCRIPTION == 'DiagnosticOdometerId'].VALUE.min())
))).reset_index()

vehicles_data['distance'] =  vehicles_data['max_distance']-vehicles_data['min_distance']
vehicles_data['fuel'] = vehicles_data['max_fuel']-vehicles_data['min_fuel']

dirty_data = vehicles_data[(pd.isna(vehicles_data['fuel'])) | (pd.isna(vehicles_data['distance'])) |
                           ((vehicles_data['distance'] == 0) &  (vehicles_data['fuel'] > 0)) |
                           ((vehicles_data['fuel'] == 0) & (vehicles_data['distance'] > 0))]

vehicles_data = vehicles_data[pd.notnull(vehicles_data['max_fuel']) & pd.notnull(vehicles_data['max_distance'])]
vehicles_data = vehicles_data[(vehicles_data['distance'] > 0) & (vehicles_data['fuel'] > 0) |  ((vehicles_data['distance'] == 0) & (vehicles_data['fuel'] == 0))]

y = np.append(vehicles_data['distance'].values,np.array(np.zeros(6500)))
xi = np.append(vehicles_data['fuel'].values,np.array(np.zeros(6500)))

A = np.vstack([xi, ones(len(xi))]).T

w = linalg.lstsq(A,y)[0]

#y = mx+b
line = (w[0]*xi+w[1])
plot(xi,line,'r-',xi,y,'o')
show()

distance_dirty_data = dirty_data[dirty_data['distance'] > 0].copy()
distance_dirty_data['fuel'] = ((distance_dirty_data['distance']-w[1])/(w[0]))

fuel_dirty_data = dirty_data[dirty_data['fuel'] > 0].copy()
fuel_dirty_data['distance'] = w[0]*fuel_dirty_data['fuel']+w[1]

print("Vehiculo con mayor rendimiento")
vehicles_data['performance'] = np.divide(vehicles_data.ix[:,'distance'],
                                         vehicles_data.ix[:,'fuel'],
                                         out=np.zeros_like(vehicles_data.ix[:,'distance']),
                                         where=(vehicles_data.ix[:,'distance']!=0))

vehicle_with_max_performance = vehicles_data.ix[vehicles_data['performance'].idxmax()]
print(vehicle_with_max_performance.VEHICLE_TYPE + " => " + str(vehicle_with_max_performance.performance))

print("Vehículos que trabajan más días")
worked_days = vehicles_data.groupby(['VEHICLE_TYPE'])['DAY'].agg(['count']).reset_index()
max_number_of_days = worked_days['count'].max()
print(worked_days[worked_days['count'] == max_number_of_days])

print("Combustible utilizado por la flota por semana")
fuel_by_week = vehicles_data.groupby(['WEEK'])['fuel'].sum()
print(fuel_by_week)

print("Correlación entre distancia/combustible")
print(str(np.corrcoef(vehicles_data['distance'],vehicles_data['fuel'])))
