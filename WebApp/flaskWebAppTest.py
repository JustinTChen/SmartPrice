from flask import Flask
from flask import render_template
from eBay.py import *

dict = calculate('iPhone+X+64+GB', 'Cell Phones & Accessories', 'New')
graph = dict['Graph']

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('test.html', Graph=graph)
