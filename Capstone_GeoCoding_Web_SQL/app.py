from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    global filename
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == None or file.filename == '':
            return render_template('index.html')
        data = pd.read_csv(file)
        colnames_list = [x.lower() for x in data.columns.values]
        if 'address' in colnames_list:
            addr_colindex = colnames_list.index('address')
            geolocator = Nominatim()
            lat_list = []
            lon_list = []
            for code in data[data.columns.values[addr_colindex]]:
                location = geolocator.geocode(code)
                if location != None:
                    lat_list.append(location.latitude)
                    lon_list.append(location.longitude)
                else:
                    lat_list.append(None)
                    lon_list.append(None)
            data['Latitude'] = lat_list
            data['Longitude'] = lon_list
            text = "Showing top 3 rows of data with calculated coordinates"
            filename = datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f" + ".csv")
            data.to_csv(filename, index = None)
        else:
            text = "No 'address' column found in a file"
            tables = []
    return render_template("index.html", table = data.head(3).to_html(), btn = "download.html", text = text)

@app.route("/download")
def download():
    return send_file(filename, attachment_filename = 'geocoded.csv', as_attachment = True)

if __name__ == '__main__':
    app.debug = True
    app.run()
