import time
from kafka import KafkaProducer, KafkaClient
import json

count = 0
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), bootstrap_servers='AWS PUBLIC DNS')
topic = 'KAFKA TOPIC'
errors = 0
continueLoop = True
TEXT_LENGTH = 100000
TERMINAL_LENGTH = 10000000

log = 'TEXT LOG FILEPATH'
w = open(log,"r")
jsontext = []
for i in range(TEXT_LENGTH): #this file size should fit into memory
    line = w.readline()
    if line == '':
        break
    try:
        jsontext.append(json.loads(line))
    except:
        continue
print(len(jsontext))
print("Finished Transcribing JSON")

start = time.time()
while continueLoop == True:
    for line in jsontext:
        hashtags = []
        try:
            for i in line['entities']['hashtags']:
                hashtags.append(i['text'].lower())
            if len(hashtags) == 0:
                pass
            else:
                payload = {'hashtags':hashtags}
                producer.send(topic, payload)
        except:
            errors += 1
        count += 1
        if count % TERMINAL_LENGTH == 0: #when to terminate the loop
            print(count, time.time() - start)
            continueLoop = False
            break
