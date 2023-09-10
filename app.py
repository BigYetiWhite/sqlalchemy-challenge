
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


##Database - From climate_starter_checkpoints.ipynb

database_path = "Resources/hawaii.sqlite"

engine = create_engine(f"sqlite:///{database_path}")
Base = automap_base()

Base.prepare(autoload_with=engine, reflect=True)



##Flask Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Resources/hawaii.sqlite"

##Variables
Measurement_class = Base.classes.measurement
Station_class = Base.classes.station
Prev_Year = '2016-08-23'
Most_Active_Station = 'USC00519281'

#Routes
#Home Page Route
@app.route("/")
def index():

    return (
        '''
        <html><head></head><body>
        <style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
        <table>
        
        <tr>
        <th><h2>Available Routes:</h2></th>
        </tr>
        <tr>
        <th><a href="/api/v1.0/precipitation">Precipitation</a><br/></th>
        </tr>
        <tr>
       <th> <a href="/api/v1.0/stations">Stations</a><br/></th>
        </tr>
        <tr>
       <th> <a href="/api/v1.0/tobs">Temperature</a><br/></th>
        </tr>
        </table>
        </body>
        '''
    )


#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement_class.date, Measurement_class.prcp).\
    filter(Measurement_class.date > Prev_Year).all()
    session.close()

    all_precipitation_readings = []
    for date, prcp in results:
        precipitation_readings = {}
        precipitation_readings["Date"] = date
        precipitation_readings["Precipitation"] = prcp    
        all_precipitation_readings.append(precipitation_readings)

    return jsonify(all_precipitation_readings)


#Stations Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results_stations = session.query(Station_class.station).all()
    session.close()
    
    all_stations = list(np.ravel(results_stations))

    return jsonify(all_stations)


###Temperature Observations Route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results_tobs = session.query(Station_class.station, Measurement_class.prcp, Measurement_class.date, Measurement_class.tobs).\
    filter(Measurement_class.station == Station_class.station).\
    filter(Measurement_class.date > Prev_Year).\
    filter(Measurement_class.station == Most_Active_Station).all()
    session.close()

    all_tobs_USC00519281_12m = []
    for station, prcp, date, tobs  in results_tobs:
        tobs_USC00519281 = {}
        tobs_USC00519281["Date"] = date
        tobs_USC00519281["Temperature"] = tobs
        tobs_USC00519281["Precipitation"] = prcp
        tobs_USC00519281["Station"] = station
        all_tobs_USC00519281_12m.append(tobs_USC00519281)

    return jsonify(all_tobs_USC00519281_12m)
    


#@app.route("/api/v1.0/<start>")
# def start(start):
#     session = Session(engine)
#     results = session.query(func.min(Measurement_class.tobs), func.avg(Measurement_class.tobs), func.max(Measurement_class.tobs)).\
#         filter(Measurement_class.date >= start).all()
#     session.close()
#     all_prcp = list(np.ravel(results))
#     return jsonify(all_prcp)

# @app.route("/api/v1.0/<start>/<end>")
# def start_end(start, end):
#     session = Session(engine)
#     results = session.query(func.min(Measurement_class.tobs), func.avg(Measurement_class.tobs), func.max(Measurement_class.tobs)).\
#         filter(Measurement_class.date >= start).filter(Measurement_class.date <= end).all()
#     session.close()
#     all_prcp = list(np.ravel(results))
#     return jsonify(all_prcp)


if __name__ == "__main__":
    app.run(debug=True)


