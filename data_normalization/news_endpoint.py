from flask import Flask
import json
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def getNewsFromMongo():
  client = MongoClient()
  db = client['news-db']

if __name__ == "__main__":
  app.run(host='localhost',port=5000,debug=True)
