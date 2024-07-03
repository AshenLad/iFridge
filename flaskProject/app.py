from flask import Flask, render_template, redirect, url_for
from query import Database
from datetime import datetime


app = Flask(__name__)


@app.route('/table')
def hello_world():  # put application's code here
    database = Database()
    data = database.quary_food()

    return render_template('table1.html', data=data)

@app.route('/')
def index():
    database = Database()
    data = database.quary_device()
    data = data[-1]
    date_object = datetime.today().date()
    date_object = str(date_object)
    return render_template('home.html', data=data, date_object=date_object)

@app.route('/device')
def hello_device():  # put application's code here
    database = Database()
    data = database.quary_device()

    return render_template('device.html', data=data)


if __name__ == '__main__':
    app.run()
