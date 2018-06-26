from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=['POST'])
def success():
    global data
    if request.method == 'POST':
        file = request.files['file']
        fname = "uploaded_" + file.filename
        file.save(secure_filename(fname))
        data = pd.read_csv(fname)
        print(data)
    return render_template("success.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
