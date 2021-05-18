#Import libraies


from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#set up for code by defining variables

app = Flask(__name__)
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement =Base.classes.measurement
Station =Base.classes.station
session = Session(engine)

#set up api
@app.route("/")
def home():
    return "The avaliable routes are /api/v1.0/precipitation, /api/v1.0/stations, /api/v1.0/tobs, /api/v1.0/<start> and /api/v1.0/<start>/<end>"

@app.route("/api/v1.0/precipitation")
def precipitation():
    dpq = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).limit(2230)
    return jsonify(dpq)

@app.route("/api/v1.0/stations")
def stations():
    stations_list = session.query(Station.name).all()
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
   tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23', Measurement.station == 'USC00519281').all()
   return jsonify(tobs_results) 

@app.route("/api/v1.0/<start>")
def start_day(start):
    
    start_results = session.query(Station.name, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs), ).filter(Measurement.date >= start).all()
    return jsonify(start_results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    start_end_results = session.query(Station.name, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs), ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_results)

