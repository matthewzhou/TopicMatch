from __future__ import print_function
import sys
from functools import partial
from itertools import combinations
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import time
from kafka import KafkaProducer, KafkaClient
import json

def sendOutput(values,topic):
    for i in values:
        producer.send(topic, bytes(i))


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='AWS KAFKA PUBLIC DNS')

    streams = []
    output = []
    sc = SparkContext(appName="SparkStreamingApp")
    ssc = StreamingContext(sc, 2)
    conf = SparkConf()
    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})
    combos = kvs.mapValues(lambda x: json.loads(x))
    counts = combos.count()
    counts.foreachRDD(lambda x: sendOutput(x.collect(),"KAFKA TOPIC FOR OVERALL WORD COUNTS"))
    combos = combos.mapValues(lambda x: x['hashtags']).flatMapValues(partial(combinations, r=2))
    combos = combos.countByValue().map(lambda x: ([x[0][1][0],x[0][1][1],x[1]]))
    counts = combos.transform(lambda rdd: rdd.sortBy(lambda x: x[2], ascending=False))
    counts.foreachRDD(lambda x: sendOutput(x.take(3),"KAFKA TOPIC FOR STREAMING HASHTAGS"))
    combos.foreachRDD(lambda x: sendOutput(x.collect(),"KAFKA TOPIC FOR WORD PAIR COUNTS"))
    ssc.start()
    ssc.awaitTermination()
