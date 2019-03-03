from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, Form, SelectField
from wtforms.validators import DataRequired
from eBay import *
from datascience import *
import numpy as np

dict = calculate('iPhone+X+64+GB', 'Cell Phones & Accessories', 'New')
graph = dict['Graph']

app = Flask(__name__)

class searchForm(Form):
    cats = list(Table().read_table('categories.csv').column('Category'))
    cats_tuples = [(cat, cat) for cat in cats]
    item = StringField('Item', validators=[DataRequired()])
    categories = SelectField('Categories', choices=cats_tuples)
    condition = SelectField('Condition', choices=[('New', 'New'), ('Used', "Used")])
    button = SubmitField('Price My Item!!')

@app.route("/")
def hello():
    form = searchForm()
    return render_template('test.html', form = form)
