from nltk import word_tokenize
import pymongo
from pymongo import MongoClient

def load_lemmas():
  lemmas_file = open("diccionarioLematizador.txt","r",encoding="utf8")
  lemma_dictionary = {}

  for line in lemmas_file:
    words_block = line.split()
    word = words_block[0]
    lemma = words_block[1]
    lemma_dictionary.update({word: lemma})

  return lemma_dictionary
    
def lemmatization(lemma_dictionary,word):
  word = word.lower()
  if word in lemma_dictionary:
    lemma = str(lemma_dictionary.get(word))
  else:
    lemma = word
  return lemma

def get_news():
  with open("noticias2.csv","r",encoding="utf8") as news_file:
    lines = news_file.readlines()

  del lines[0]

  return lines

def get_stop_words():
  with open("stopwords.txt","r",encoding="utf8") as stop_words_file:
    stop_words = stop_words_file.readlines()
    for index in range(0,len(stop_words)):
      stop_words[index] = stop_words[index].rstrip()

  return set(stop_words)
      
def remove_stop_words(stop_words,line):
  return [word for word in line if word not in stop_words]

def get_document_and_dictionary():
  news = get_news()
  stop_words = get_stop_words()  
  document = []
  lemmas_dictionary = load_lemmas()
  dictionary = {}

  for i,new in enumerate(news):
    new = new.lower()
    tokens = word_tokenize(new)
    tokens = remove_stop_words(stop_words,tokens)

    if(len(tokens) > 0):
      new_dictionary = {}

      for index in range(0,len(tokens)):
        token_lemma = lemmatization(lemmas_dictionary,tokens[index])
        new_dictionary[token_lemma] = 1
        if(tokens[index] not in dictionary):
          dictionary[tokens[index]] = 1

      document.append({"id": i,"words": new_dictionary, "text": new})

  return {'dictionary': dictionary,
          'document': document}


def save_document_matrix(document,dictionary):
  document_matrix = []
  client = MongoClient()
  db = client["news-db"]
  news_collection = db["news"]
  dictionary_collection = db["dictionary"]
  
  for line in document:
    line_vector = []
    for word in dictionary:
      if word in line['words']:
        line_vector.append(1) 
      else:
        line_vector.append(0)

    news_collection.insert_one({"text": line["text"],
                                "vector": line_vector})

  dictionary_collection.insert_one({"dictionary": dictionary})

document_and_dictionary = get_document_and_dictionary()
document = document_and_dictionary['document']
dictionary = sorted(document_and_dictionary['dictionary'])
  
save_document_matrix(document,dictionary)

