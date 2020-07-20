from wtforms import Form, validators, DateField, DateTimeField, DecimalField
from wtforms.validators import InputRequired

class QuickBooksForm(Form):
    period = DateField('period', [validators.DataRequired()])
    wisetack_junior_position = DecimalField('wisetack_junior_position', validators=[InputRequired()])
    lighter_junior_position = DecimalField('lighter_junior_position',  validators=[InputRequired()])
    