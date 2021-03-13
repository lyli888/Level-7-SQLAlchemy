#Import Dependencies
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
    """Welcome to my Hawaii Climate App. Step into my office!"""
    return (
        f"Available Routes:<br/>"
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

    """See Precipitation By Date"""
    #Query Precipitation
    precipitation_results = session.query(Measurement.prcp).all()

    session.close()
    
    #Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

    all_precipitation = []
    for name, age, sex in results:
        precipitation_dict = {}
        passenger_dict["date"] = date
        passenger_dict["prcp"] = prcp
        all_precipitation.append(passenger_dict)

    return jsonify(all_precipitation)

#List Stations
@app.route("/api/v1.0/stations")
def stations():
    
    """All Stations"""
    
    session = Session(engine)
    
    station_results = session.query(Station.station, Station.name).all()
    
    session.close()
    
    return jsonify(s_results)

    @app.route("/api/v1.0/tobs")

def tobs():
    
    """Temperature Over Past Year Of Data"""
    
    session = Session(engine)
    
    prev_year_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    tobs_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= prev_year_date).all()
    
    session.close()
    
    return jsonify(tobs_results)

if __name__ == '__main__':
    app.run(debug=True)
