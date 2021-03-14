#Import Dependencies
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
from datetime import timedelta

import pandas as pd
import numpy as np

#Create engine, reflect the tables 
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect an existing database into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect=True)

#Save references to tables 'Station' & "Measurement"
Station = Base.classes.station
Measurement = Base.classes.measurement

#Flask Setup
app = Flask(__name__)

#List all available routes
@app.route("/")
def welcome():
    return (
        f"Welcome to Ly's Hawaii Climate App! Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end>"
    )

#Precipitation By Date
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query Precipitation
    precipitation_results = session.query(Measurement.date, Measurement.prcp).all()   
    #Close Session
    session.close() 
    #Convert the query results to a dictionary using `date` as the key and `prcp` as the value.  
    pdict = dict(precipitation_results)   
    return jsonify(pdict)


#List Stations
@app.route("/api/v1.0/stations")
def stations():  
    session = Session(engine)
    station_results = session.query(Station.station, Station.name).all()
    session.close()  
    return jsonify(station_results)


#Temperature Past Year
@app.route("/api/v1.0/tobs")
def tobs():   
    session = Session(engine)
    tobs_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    session.close()
    return jsonify(tobs_results)

#Start
@app.route("/api/v1.0/start/<start_date>")
def weather(start_date):
    session = Session(engine)
    weather_condition = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    weather_since = list(np.ravel(weather_condition))
    session.close() 
    return jsonify(weather_since)

#Start/End
@app.route("/api/v1.0/start/end/<start>/<end>")
def condition(start, end):
    session = Session(engine)
    weather = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    weather_betweendates = list(np.ravel(weather))
    return jsonify(weather_betweendates)

if __name__ == '__main__':
    app.run(debug=True)
