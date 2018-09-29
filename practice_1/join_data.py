import pandas as pd
import glob,os

fileData = pd.DataFrame()
data = []

for status_file in glob.glob(os.path.join(".","*.csv")):
  dataFrame = pd.read_csv(status_file, index_col=None, header=None)
  data.append(dataFrame)

fileData = pd.concat(data)

fileData.to_csv("StatusDataComplete.csv",header=False,index=False)

