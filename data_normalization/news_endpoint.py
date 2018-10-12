from flask import Flask
from flask import jsonify
import pymongo
import numpy as np
import math
from pymongo import MongoClient
from nltk import word_tokenize

app = Flask(__name__)

client = MongoClient()
app.config.update(JSON_AS_ASCII = False)
dictionary = []
np.seterr(divide='ignore', invalid='ignore')

@app.route("/news/<query>")
def get_news(query):
  query_vector = build_query_vector(query)
  related_news = []
  news = get_news_from_mongo()

  for new in news:
    cosine_similarity = get_cosine_similarity(query_vector,new['vector'].copy())
    if(cosine_similarity > 0):
      related_news.append({'new': new['text'],
                           'cosine_similarity': cosine_similarity})

  n = (10 if len(related_news) >= 10 else len(related_news))

  related_news = sorted(related_news,reverse=True,key=lambda k: k['cosine_similarity'])[0:n]

  def get_new_from_map(new):
    new.pop('cosine_similarity',None)
    return new

  related_news  = list(map(get_new_from_map, related_news))

  return jsonify(related_news)


def get_news_from_mongo():
  db = client['news-db']
  news_collection = db['news']
  return news_collection.find({})

def get_dictionary_from_mongo():
  db = client['news-db']
  dictionary = db['dictionary']
  return dictionary.find_one()

def build_query_vector(query):
  query_words = word_tokenize(query)
  query_words_dict = {}
  query_vector = []

  for word in query_words:
   query_words_dict[word] = 1

  for word in dictionary['dictionary']:
    if word in query_words_dict.keys():
      query_vector.append(1)
    else:
      query_vector.append(0)

  return query_vector

def get_cosine_similarity(query_vector,document_vector):
  dot_product = np.sum(np.multiply(query_vector,document_vector))
  query_vector_norm = np.sum(np.multiply(query_vector,query_vector))
  document_vector_norm = np.sum(np.multiply(document_vector,document_vector))
  cosine_similarity = np.divide(dot_product,math.sqrt(query_vector_norm*document_vector_norm))
  return cosine_similarity

if __name__ == "__main__":
  dictionary = get_dictionary_from_mongo()
  app.run(host='localhost',port=5000,debug=True)
