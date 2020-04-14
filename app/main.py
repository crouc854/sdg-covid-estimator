from flask import Flask, request, jsonify, Response, g
from flask_restful import Resource, Api, reqparse
from src.estimator import estimator
import time
import json
from dicttoxml import dicttoxml

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return "<h1>Welcome!!</h1>"

@app.route('/api/v1/on-covid-19', methods=['GET', 'POST'])
@app.route('/api/v1/on-covid-19/json', methods=['GET', 'POST'])
def estimate():
    if request.method =='POST':
        data = request.get_json(force=True)
        return json.dumps(estimator(data)), {'Content-Type':'application/json'}

@app.route('/api/v1/on-covid-19/xml', methods=['GET', 'POST'])
def estimateXml():
    if request.method =='POST':
        data = estimator(request.get_json(force=True))
        return dicttoxml(data), {'Content-Type':'application/xml'}

@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def get_logs():
    f = open("log.txt", "r").read()
    return Response(f, mimetype="text/plain")

@app.before_request
def start_timer():
    g.start = int(round(time.time() * 1000))

@app.after_request
def log_requests(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path == '/robots.txt':
        return response
    elif request.path.startswith('/static'):
        return response

    now = int(round(time.time() * 1000))
    duration = now - g.start
    if duration < 10 and duration > 0:
        duration = "0"+str(duration)
    method = request.method
    resp_code = response.status_code
    request_url = request.path
    
    with open("log.txt", "a+") as f:
        f.write(f"{method}\t{request_url}\t{resp_code}\t{duration}ms\n")
        f.close()
    return response