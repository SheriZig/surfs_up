import datetime as dt
from typing_extensions import runtime
import flask
import numpy as np
import pandas as pd

## SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy import engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask dependencies
from flask import Flask, jsonify

# Set up the database engine to access sqlite data file
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the DATABASE into our classes
Base = automap_base()

# Reflect the TABLES
Base.prepare(engine, reflect=True)

# Save the references to each table so we can type reference
# instead of Base.classes.measurement
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from PYTHON to DATABASE
session = Session(engine)

# Create a Flask application called 'app'
app = Flask(__name__)

# Create the root/homepage route for the application site 
# Use function 'welcome' to define additional routes
# Add routing information for each of the other routes
# /api/v1.0/ represents version 1 of our application and can be 
# updated for future versions
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')


# Run Application
# Be sure to navigate to the project folder that 
# contains the app.py file
# Run the command (without '') 'flask run' in the TERMINAL

# Create the route for PRECIPITATION analysis
# Create dictionary with date as key precipitation as the value
# jsonify the dictionary = a function that converts dictionary to JSON File
# Jsonify()
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create route for the STATIONS analysis
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create route for TOBS analysis
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create route for Start/End dates
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
     
