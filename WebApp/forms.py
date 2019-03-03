from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class itemForm(FlaskForm):
    item = StringField("Item:", validators=[DataRequired()])
    button = SubmitField("Price Your Item!")
