import findspark
import random
findspark.init()
from pyspark.ml.fpm import FPGrowth
from pyspark.mllib.fpm import PrefixSpan
from pyspark import SparkContext, SQLContext, SparkConf
from pyspark.sql import Row

conf = SparkConf()
spark_context = SparkContext(conf=conf)
sql_spark_context = SQLContext(spark_context)

def getItems(itemsRange,itemsNumber):
  return random.sample(range(1,itemsRange+1),itemsNumber)

def getTransactions(numberOfTransactions,
                    numberOfItems,
                    transactionSize):
  rows = list()
  for i in range(0,numberOfTransactions):
    rows.append(Row(id=i,items=getItems(numberOfItems,
                                        transactionSize)))

  return rows

def createRowsList(numberOfTransactions,
                   numberOfItems,
                   transactionSize):
  rows = list()
  for i in range(0,numberOfTransactions):
    column = list()
    for i in range(0,random.randrange(1,transactionSize+1)):
      column.append(getItems(numberOfItems,
                             random.randrange(1,transactionSize+1)))
    rows.append(column)

  return rows

transactions = getTransactions(10,8,5)

df = sql_spark_context.createDataFrame(transactions)

df.show()

fpGrowth = FPGrowth(itemsCol="items",
                    minSupport=0.7,
                    minConfidence=0.6)

model = fpGrowth.fit(df)

print("Frequent Itemset")
model.freqItemsets.show()

print("Association rules")
model.associationRules.show()

print("Predictions generated from association rules")
model.transform(df).show()


rows_list = createRowsList(10,8,5)
data = spark_context.parallelize(rows_list)

prefixSpan = PrefixSpan.train(data,0.5,5,32000000)


print("Frequent sequential patterns")
for sequence in prefixSpan.freqSequences().collect():
  print(str(sequence.sequence) + "=>" + str(sequence.freq))

