from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, Form, SelectField
from wtforms.validators import DataRequired
from eBay import *
from datascience import *
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'flask-is-hard'


class searchForm(FlaskForm):
    cats = list(Table().read_table('categories.csv').column('Category'))
    cats_tuples = [(cat, cat) for cat in cats]
    item = StringField('Item', validators=[DataRequired()])
    categories = SelectField('Categories', choices=cats_tuples)
    condition = SelectField('Condition', choices=[('New', 'New'), ('Used', "Used")])
    submit = SubmitField('submit')



@app.route("/", methods=['GET', 'POST'])
def Home():
    form = searchForm()
    if form.validate_on_submit():
        Item = form.item.data
        Cat = form.categories.data
        Cond = form.condition.data
        results = calculate(Item, Cat, Cond)
        return render_template('page2.html', image=results['Graph'] , mean=results['Mean'],SD=results['SD'],quarter=results['25%'], half=results['50%'], threequarters=results['75%'], min=results['Min'], max=results['Max'])

    return render_template('test.html', form = form)
