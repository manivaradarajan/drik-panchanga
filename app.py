import example
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/v1/panchangam/date/<string:date_str>")
def panchangam_date(date_str):
    # city = request.args.get('city')
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    timezone = request.args.get('timezone')
    return example.basic_panchangam(date_str, latitude, longitude, timezone)


