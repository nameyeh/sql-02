# Import dependencies

import pandas as pd
import numpy as np
import datetime as datetime
import os

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc

from flask import Flask, jsonify

# Flask Setup #################################################
app = Flask(__name__)

# Database connection steps

# Connect to sqlite database using create_engine 
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare the base using automap
Base = automap_base()

# Reflect the database tables into classes
Base.prepare(engine, reflect=True)

# Assign classes to variables, save a reference 

measurement = Base.classes.Measurement
station = Base.classes.Station

# Create a session

session = Session(engine)

# Flask Routes #################################################


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_dt/<start><br/>"
        f"/api/v1.0/dt_range/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data.
    # Select only the date and prcp values.
    
    prcp_q = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > '2017-04-14').group_by(measurement.date).\
    order_by(measurement.date).all()

    # Create a dictionary from the row data and append to a list 
    prcp_list = []
    for row in prcp_q:
        prcp_dict = {}
        prcp_dict["date"] = measurement.date
        prcp_dict["prcp"] = measurement.prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    # Return a json of stations
    station_list = session.query(station.station, station.name).all()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Return a json of tobs from the last year
    tobs_q = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > '2017-04-14').order_by(measurement.date).all()
    return jsonify(tobs_q)


@app.route("/api/v1.0/start/<start>")
def start_date(start):
# Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.



# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    temp_min = session.query(func.min(measurement.tobs)).\
        filter(measurement.date == start).first()
    temp_max = session.query(func.max(measurement.tobs)).\
        filter(measurement.date == start).first()
    temp_avg = session.query(func.avg(measurement.tobs)).\
        filter(measurement.date == start).first()
    return jsonify(temp_min, temp_max, temp_avg)

@app.route("/api/v1.0/dt_range/<start>/<end>")
def dt_range(start, end):
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

    temp_min = session.query(func.min(measurement.tobs)).\
        filter(measurement.date.between(start, end)).first()
        
    temp_max = session.query(func.max(measurement.tobs)).\
        filter(measurement.date.between(start, end)).first()
        
    temp_avg = session.query(func.avg(measurement.tobs)).\
        filter(measurement.date.between(start, end)).first()
        
    return jsonify(temp_min, temp_max, temp_avg)

if __name__ == '__main__':
    app.run(debug=True)

