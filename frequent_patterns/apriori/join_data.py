import pandas as pd
import glob,os
from datetime import datetime

sales = pd.DataFrame()
sales_data = []

for sales_file in glob.glob(os.path.join(".","sales*")):
  data_frame = pd.read_csv(sales_file,
                           sep="|",
                           header=0)
  sales_data.append(data_frame)

sales = pd.concat(sales_data)
sales['date'] = pd.to_datetime(sales['the_date'],format='%Y-%m-%d %H:%M:%S')
sales['week'] = sales['date'].dt.week
sales.drop(columns=['the_date'])

sales.to_csv("Sales.csv",index=False)

