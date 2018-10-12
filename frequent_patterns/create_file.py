import pandas as pd
import numpy as np
from pandas import pivot_table

sales = pd.read_csv("Sales.csv")

sales_by_date = sales.groupby(['the_year',
                               'the_month',
                               'day_of_month',
                               'the_day',
                               'store_id',
                               'product_id']).product_id.agg(['count']).reset_index()

sales_by_date = sales_by_date[~sales_by_date.the_day.isin(["Saturday","Sunday"])]

sales_by_date = sales_by_date[['the_year','the_month','day_of_month','store_id','product_id','count']]

rules  = pivot_table(sales_by_date,values = 'count', index=['the_year','the_month','day_of_month','store_id'],
                     columns = ['product_id']).reset_index()

rules = rules.drop(["the_year","the_month","day_of_month","store_id"],axis=1)

rules = rules.fillna(0)
rules[rules >= 1.0] = "SI"
rules[rules == 0] = "NO"

rules.columns = ["L" + str(col) for col in rules.columns]
rules.to_csv("rules.csv",index=False)

