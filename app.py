import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt




engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

measurementClass = Base.classes.measurement
stationClass = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )

@app.route("/api/v1.0/precipitation")

def precip():
	new_final_time = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
	precinfo = session.query(measurementClass.date, measurementClass.prcp).filter(measurementClass.date > new_final_time).all()
	precdict = {date: prcp for (date, prcp) in precinfo}
	return jsonify(precdict)

@app.route("/api/v1.0/stations")

def stations():
	stationsinfo2 = session.query(stationClass.station).all()
	return jsonify(stationsinfo2)


@app.route("/api/v1.0/tobs")
def temp():

	new_final_time = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
	tempinfo = session.query(measurementClass.tobs).\
	filter(measurementClass.station == 'USC00519281').\
	filter(measurementClass.date > new_final_time).all()
	return jsonify(tempinfo)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>`")
def stats(start=None, end=None):
	if not end:
#when user does not pass enddate
	tmin = session.query(func.min(measurementClass.tobs)).\
	filter(measurementClass.date >= start).all()
	tavg = session.query(func.avg(measurementClass.tobs)).\
	filter(measurementClass.date >= start).all()
	tmax = session.query(func.max(measurementClass.tobs)).\
	filter(measurementClass.date >= start).all()
	return jsonify(tmin)
	return jsonify(avg)
	return jsonify(tmax)

	else:
#when user passes end date
	tmin = session.query(func.min(measurementClass.tobs)).\
	filter(measurementClass.date >= start and measurementClass.date <= end).all()
	tavg = session.query(func.avg(measurementClass.tobs)).\
	filter(measurementClass.date >= start and measurementClass.date <= end).all()
	tmax = session.query(func.max(measurementClass.tobs)).\
	filter(measurementClass.date >= start and measurementClass.date <= end).all()
	return jsonify(tmin)
	return jsonify(avg)
	return jsonify(tmax)


if __name__ == '__main__':
	app.run(debug=True)


















