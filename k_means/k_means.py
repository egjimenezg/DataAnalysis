import numpy as np
import findspark
findspark.init()
import pyspark
import random
import matplotlib.pyplot as plt
import itertools

from math import sqrt
from numpy import array

# Function that selects the centroids randomly
# from the input
def getKCentroids(k,data):
  centroids = []
  data_size = len(data)

  for index in random.sample(range(0,data_size),3):
    centroids.append(data[index])

  return centroids

# Euclidean distance
def euclidean_distance(p,q):
  if p.size != q.size:
    raise ValueError("The vectors must have the same dimensions")
  else: 
    return np.sqrt(np.sum((p-q)**2))

# Assign point to each cluster
def createClusters(data,centroids):
  clusters = []

  for n in range(0,len(centroids)):
    clusters.append([])
  
  for point in data:
    distances_to_centroid = []
    for centroid in centroids:
      distances_to_centroid.append(euclidean_distance(point,centroid))

    point_cluster = distances_to_centroid.index(min(distances_to_centroid))
    clusters[point_cluster].append(point)

  return clusters

def getDifferencePercentage(previous_centroid,current_centroid):
  return np.absolute(np.sum((previous_centroid-current_centroid)/current_centroid * 100))


# Algorithm implementation for n dimensions vector and k number of clusters
spark_context = pyspark.SparkContext(appName="kMeans")
input_lines =  spark_context.textFile("input.txt")

minDifference=5 #Difference between clusters of previous and current iteration
                #set to 5%

k = 3 # Number of clusters
data = input_lines.map(lambda line: array([float(point) for point in line.split(" ")]))
data = data.collect()
iterations = 20
iteration = 0
valid_centroids = False

while(iteration < iterations and (not valid_centroids)):
  valid_centroids = True
  centroids = getKCentroids(k,data)
  clusters = createClusters(data,centroids)
  last_centroids = centroids.copy()

  for cluster in range(0,len(clusters)):
    centroids[cluster] = np.average(clusters[cluster],axis=0)

  for centroid in range(0,len(centroids)):
    previous = last_centroids[centroid]
    difference_percentage = getDifferencePercentage(previous,centroids[centroid])
   
    if(difference_percentage > minDifference):
      valid_centroids = False       
    
  iteration +=1;

# Plot 
for centroid in centroids:
  plt.scatter(centroid[0],centroid[1],s=50,marker="x")

colors = itertools.cycle(["r","g","b"])

for cluster in range(0,len(clusters)):
  color = next(colors)
  for point in clusters[cluster]:
    plt.scatter(point[0],point[1],color=color,s=20)

plt.show()
