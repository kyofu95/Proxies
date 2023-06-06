from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional


class FilterForm(FlaskForm):
    country = StringField("Country", validators=[Optional()])
    protocol = StringField("Protocol", validators=[Optional()])
