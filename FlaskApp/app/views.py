from app import app
from flask import Flask, jsonify, render_template, request, redirect
import time, math
from kafka import KafkaConsumer, KafkaClient


@app.route('/_timeseries')
def timeseries():
    """Retrieve time series for currKey"""
    cumulative = []
    hashtags = []
    count = 0
    consumer = KafkaConsumer(bootstrap_servers ='ec2-34-225-221-200.compute-1.amazonaws.com',auto_offset_reset='latest')
    consumer.subscribe(['streaming-outputs1'])
    for msg in consumer:
        cumulative.append(int(msg[6].decode('utf-8')))
        break
    consumer.subscribe(['hashtags'])
    for msg in consumer:
        count += 1
        hashtags.append(msg[6].decode('utf-8'))
        if count == 4:
            break
    consumer.close()
    return jsonify(cumulative = cumulative,hashtags = hashtags)

# returns slide deck as redirect for easy access
@app.route('/deck')
def deck():
 return redirect("https://docs.google.com/presentation/d/1wEBlqWDfi3yLH2jh9gWsPNJ0S1LYAgoQQjFCy6CG-iY/edit?usp=sharing")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
