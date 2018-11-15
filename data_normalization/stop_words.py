class StopWords:

  def __init__(self,spark):
    self.stop_words = self.get_stop_words(spark)
 
  def get_stop_words(self,spark):
    stop_words = spark.sparkContext.textFile("stopwords.txt")
    stop_words = stop_words.map(lambda word: word.rstrip().lower())
    return set(stop_words.collect())

  def remove_stop_words(self,line):
    return [word for word in line if word not in self.stop_words]
