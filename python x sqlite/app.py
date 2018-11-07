import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

Base = automap_base()

Base.prepare(engine, reflect=True)

Precipitation = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Precipitation).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for precip in results:
        precipitation_dict = {}
        precipitation_dict["date"] = precip.date
        precipitation_dict["prcp"] = precip.prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/station")
def stations():
    results = session.query(Station).all()
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation 
        all_stations.append(station_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query all passengers
    results = session.query(Precipitation).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_temp = []
    for temp in results:
        temp_dict = {}
        temp_dict["date"] = temp.date
        temp_dict["tobs"] = temp.tobs
        all_temp.append(temp_dict)

    return jsonify(all_temp)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    results = session.query(Precipitation.tobs).filter(Precipitation.date >= start).all()

    list_of_temp = []
    for i in results:
        list_of_temp.append(i[0])

    temp_dict = {}
    temp_dict["min_temp"] = min(list_of_temp)
    temp_dict["avg_temp"] = sum(list_of_temp)/len(list_of_temp)
    temp_dict["max_temp"] = max(list_of_temp)
    return jsonify(temp_dict)    

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    results = session.query(Precipitation.tobs).filter(Precipitation.date >= start).filter(Precipitation.date <= end).all()

    list_of_temp = []
    for i in results:
        list_of_temp.append(i[0])

    temp_dict = {}
    temp_dict["min_temp"] = min(list_of_temp)
    temp_dict["avg_temp"] = round(sum(list_of_temp)/len(list_of_temp), 1)
    temp_dict["max_temp"] = max(list_of_temp)
    return jsonify(temp_dict)    

