from nltk import word_tokenize
import pymongo
from pymongo import MongoClient
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from lemmatizer import Lemmatizer
from stop_words import StopWords

def get_tokenized_news(spark):
  news = spark.sparkContext.textFile("noticias100.csv")
  news = news.map(lambda new: {"text": new,
                               "words": word_tokenize(new.lower())})

  return news.collect()

def lemmatize_new(lemmatizer,new):
  new_dict = {}
  for index in range(0,len(new["words"])):
    new_dict[lemmatizer.lemmatization(new["words"][index])] = 1
  
  return {"text": new["text"], "words": new_dict}


def get_document_and_dictionary(spark):
  news = spark.sparkContext.parallelize(get_tokenized_news(spark))
  stop_words = StopWords(spark)
  news_without_stop_words = news.map(lambda new: {"text": new["text"],
                                                  "words":stop_words.remove_stop_words(new["words"])})

  lemmatizer = Lemmatizer()
  lemmatized_news = news_without_stop_words.map(lambda new: lemmatize_new(lemmatizer,
                                                                          new))

  news_words = lemmatized_news.flatMap(lambda new: new["words"])\
                              .distinct()

  dictionary = list(news_words.map(lambda word: (word, 1))\
                              .collect())

  return {"dictionary": dictionary,
          "document": lemmatized_news.collect()}

def createVector(new, dictionary):
  new_vector = []
  for word in dictionary:
    if word[0] in new["words"]:
      new_vector.append(1)
    else:
      new_vector.append(0)
  return new_vector

def save_document_matrix(spark,document,dictionary):
  client = MongoClient()
  db = client["news-db"]
  news_collection = db["news"]
  dictionary_collection = db["dictionary"]
  
  tokenized_news = spark.sparkContext.parallelize(document)
  document_matrix = tokenized_news.map(lambda new: {"text": new["text"],
                                                    "vector": createVector(new,dictionary)})

  news_collection.insert_many(document_matrix.collect())
  
  dictionary_collection.insert_one({"dictionary": dictionary})



spark = SparkSession.builder.appName("Information Retrieval").getOrCreate()

document_and_dictionary = get_document_and_dictionary(spark)
document = document_and_dictionary["document"]
dictionary = sorted(document_and_dictionary["dictionary"])

save_document_matrix(spark,document,dictionary)

spark.stop()
