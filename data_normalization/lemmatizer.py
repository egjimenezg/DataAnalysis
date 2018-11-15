class Lemmatizer:
  
  def __init__(self):
    lemmas_file = open("diccionarioLematizador.txt","r",encoding="utf8")
    lemma_dictionary = {}
    
    for line in lemmas_file:
      words_block = line.split()
      word = words_block[0]
      lemma = words_block[1]
      lemma_dictionary.update({word: lemma})
   
    self.lemma_dictionary = lemma_dictionary 


  def lemmatization(self,word):
    word = word.lower()
    if word in self.lemma_dictionary:
      lemma = str(self.lemma_dictionary.get(word))
    else:
      lemma = word
    return lemma
