import pandas as pd

fileData = pd.DataFrame()
data = []

for i in range(1,5):
  dataFrame = pd.read_csv("StatusData" + str(i) + ".csv", index_col=None, header=0)
  data.append(dataFrame)

fileData = pd.concat(data)

fileData.to_csv("StatusDataComplete.csv")

