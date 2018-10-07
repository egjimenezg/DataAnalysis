import numpy as np
import pandas as pd
import operator

data = pd.read_csv("data.csv",header=None)

def classify(v,k,distance):
  target_values = data.iloc[:,-1]
  nearest_neighbors = knn(data,k,v,distance)
  classification_values = {}
  
  for index in nearest_neighbors:
    if target_values[index] not in classification_values.keys():
      classification_values[target_values[index]] = 1
    else:
      classification_values[target_values[index]] += 1

  return max(classification_values.items(),key=operator.itemgetter(1))[0]


def knn(vectors,k,vector_to_classify,distance):
  distances = []
  for i in range(0,len(vectors)):
    x = vectors.loc[i,:]
    x = x[0:len(x)-1]

    distances.append({"index": i,
                      "value": distance(x,vector_to_classify)})

  distances = sorted(distances,key=lambda x:x['value'], reverse=True)
  indexes = list(map(lambda distance: distance['index'],distances[0:k]))
  return indexes

def euclidean_distance(x,y):
  summation = 0
  for i in range(0,x.size):
    summation += ((x[i] - y[i])**2)

  return (summation)**(1/2)

vectors_to_classify = [np.array([1100000,60,1,2,1,500]),
                       np.array([1100000,60,1,2,1,500]),
                       np.array([1800000,65,1,2,1,1000]),
                       np.array([2300000,72,1,3,1,1400]),
                       np.array([3900000,110,2,3,1,1800])]

for k in [1,3,5]:
  for v in vectors_to_classify:
    classify(v,k,euclidean_distance)
