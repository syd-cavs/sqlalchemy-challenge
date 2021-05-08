import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home_page():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_results = session.query(measurement.date, measurement.prcp).all()
    session.close()
    
    all_dates = {date:prcp for date, prcp in prcp_results}
    
    precipitation = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify([precipitation])


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_results = session.query(measurement.date, measurement.tobs).all()
    session.close()
    
    year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)
    last_day = session.query(measurement.date).order_by(measurement.date.desc()).first()
    precipitation = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > year_ago).order_by(measurement.date).all()

    tobs_tobs = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Observations"] = tobs
        precipitation.append(tobs_dict)

    return jsonify([tobs_tobs])

if __name__ == '__main__':
    app.run(debug=True)
