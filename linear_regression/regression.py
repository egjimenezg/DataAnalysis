from sklearn import linear_model
from sklearn import preprocessing
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stats
import itertools

dataPeople = pd.read_csv("data/clientes.csv")    # Reading the data

dataPeople = dataPeople.drop(["Obs No."],axis=1)

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
income_scaled = min_max_scaler.fit_transform(dataPeople["Income"].values.astype(float).reshape(-1,1))
residence_length_scaled = min_max_scaler.fit_transform(dataPeople["Residence Length"].values.astype(float).reshape(-1,1))

dataPeople["Income"] = income_scaled[:,0]
dataPeople["Residence Length"] = residence_length_scaled[:,0]

characteristics = list(dataPeople.columns.values)
characteristics.remove("Buy")
max_accuracy_value = 0
max_accuracy_characteristics = []
accuracy = 0

for i in range(1,len(characteristics)+1):
  combinations = list(itertools.combinations(characteristics,i))
  for combination in combinations:
    features = []
    for item in combination: 
      features.append(dataPeople[item])

    log_model = linear_model.LogisticRegression(solver='liblinear')
    train_features =  pd.DataFrame(features).T

    log_model.fit(X = train_features,
                  y = dataPeople["Buy"])
 
    accuracy = log_model.score(X=train_features,
                              y=dataPeople["Buy"])

    if(accuracy > max_accuracy_value):
      max_accuracy_value = accuracy
      max_accuracy_characteristics = combination

print("Max accuracy value " + str(max_accuracy_value))
print("Characteristics " + str(max_accuracy_characteristics))

