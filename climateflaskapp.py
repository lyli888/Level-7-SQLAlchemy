#Import Dependencies
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

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
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )

#Precipitation By Date
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query Precipitation
    precipitation_results = session.query(Measurement.prcp).all()

    #Close Session
    session.close()
    
    #Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

    precipitation_dict = {}
    date_list = []
    prcp_list = []
    
    for date in precipitation_results:
        
        current_date = precipitation_results["date"] 
        current_prcp = int(precipitation_results["prcp"])
        
        precipitation_dict = precipitation_dict.append{current_date:current_prcp}

    return jsonify(precipitation_dict)

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
    prev_year_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    prev_year_date = dt.date(prev_year_date) - dt.timedelta(days=365)
    tobs_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= prev_year_date).all()
    session.close()
  
    return jsonify(tobs_results)

#Start
@app.route("/api/v1.0/<start>")
def start(date):
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(day_temp_results)

#Start/End
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(multi_day_temp_results)

if __name__ == '__main__':
    app.run(debug=True)
