from flask import Flask
from flask import jsonify
import pymongo
import numpy as np
import math
from pymongo import MongoClient
from nltk import word_tokenize
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from stop_words import StopWords
from lemmatizer import Lemmatizer

np.seterr(divide='ignore', invalid='ignore')

app = Flask(__name__)
app.config.update(JSON_AS_ASCII = False)

client = MongoClient()

dictionary = []
spark = None 
stop_words = None
lemmatizer = None


@app.route("/news/<query>")
def get_news(query):
  query_vector = build_query_vector(query)

  news = spark.sparkContext.parallelize(get_news_from_mongo())
  related_news = news.map(lambda new: {"cosine_similarity": get_cosine_similarity(query_vector,
                                                                          new["vector"].copy()),
                                       "new": new["text"]})\
                     .filter(lambda new: new["cosine_similarity"] > 0)\
                     .collect()
             

  n = (10 if len(related_news) >= 10 else len(related_news))

  related_news = sorted(related_news,reverse=True,key=lambda k: k['cosine_similarity'])[0:n]
  related_news = spark.sparkContext.parallelize(related_news)

  def get_new_from_map(new):
    new.pop('cosine_similarity',None)
    return new

  related_news  = related_news.map(get_new_from_map).collect()

  return jsonify(related_news)

def get_news_from_mongo():
  db = client['news-db']
  news_collection = db['news']
  return news_collection.find({})

def get_dictionary_from_mongo():
  db = client['news-db']
  dictionary = db['dictionary']
  return dictionary.find_one()

def get_query_vector(dictionary_word, query):
  if dictionary_word in query:
    return 1
  else:
    return 0

def build_query_vector(query):
  query_words = word_tokenize(query)
  query_words = stop_words.remove_stop_words(query_words)

  query_words = list(map(lemmatizer.lemmatization,query_words))

  dictionary_rdd = spark.sparkContext.parallelize(dictionary["dictionary"])
  dictionary_words = dictionary_rdd.map(lambda word: word[0])
  rdd_query = dictionary_words.map(lambda word: get_query_vector(word,query_words))
  return rdd_query.collect() 
  
def get_cosine_similarity(query_vector,document_vector):
  dot_product = np.sum(np.multiply(query_vector,document_vector))
  query_vector_norm = np.sum(np.multiply(query_vector,query_vector))
  document_vector_norm = np.sum(np.multiply(document_vector,document_vector))
  cosine_similarity = np.divide(dot_product,math.sqrt(query_vector_norm*document_vector_norm))
  return cosine_similarity

if __name__ == "__main__":
  dictionary = get_dictionary_from_mongo()
  spark = SparkSession.builder.appName("News endpoint")\
                    .getOrCreate()

  stop_words = StopWords(spark)
  lemmatizer = Lemmatizer()

  app.run(host='localhost',port=5000,debug=True)
