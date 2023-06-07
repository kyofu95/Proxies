from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional


class FilterForm(FlaskForm):
    """A WTF form for filtering data based on country and protocol."""

    country = StringField("Country", validators=[Optional(strip_whitespace=False)])
    protocol = StringField("Protocol", validators=[Optional()])
