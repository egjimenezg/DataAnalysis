import mysql.connector
import pandas as pd

database = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd=""
)

cursor = database.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS FREQUENT_PATTERNS;")

database.database = "FREQUENT_PATTERNS"

table_query = """CREATE TABLE IF NOT EXISTS TRANSACTION (
  ID INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  YEAR INT(5),
  MONTH INT(2),
  WEEK INT(2),
"""

sales = pd.read_csv("Sales.csv")
products_number = len(sales.product_id.unique())

for index,product_id  in enumerate(sorted(sales.product_id.unique())):
  table_query += "T_" + str(product_id) + " INT(6) "
  if(index == products_number-1):
    table_query += ") ENGINE=MyISAM;\n"
  else:
    table_query += ",\n"

cursor.execute(table_query)

database.close()

