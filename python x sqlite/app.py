from flask import Flask, jsonify
import csv

app = Flask(__name__)

from numpy import loadtxt
key_value = loadtxt("Resources/hawaii_prcp.csv", delimiter=",")
prcp_dict = { k:v for k,v in key_value }

@app.route("/api/v1.0/precipitation")
def jsonified():
    return jsonify(prcp_dict)