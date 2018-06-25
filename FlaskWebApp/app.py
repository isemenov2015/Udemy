from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dfuyth@localhost/height_collector'
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key = True)
    email_ = db.Column(db.String(120), unique = True)
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods = ['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_name"]
        #print(email, height)
        #put values in a database
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            #calculate average height
            avg_height = round(db.session.query(func.avg(Data.height_)).scalar(), 1)
            count = db.session.query(Data).count()
            send_email(email, height, avg_height, count)
            return render_template("success.html")
        else:
            return render_template("index.html", text = "Duplicate email. We already have data from this address")

if __name__ == '__main__':
    app.debug = True
    app.run()
