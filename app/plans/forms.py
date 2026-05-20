from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class PlanForm(FlaskForm):
    name = StringField('Plan Name', validators=[
        DataRequired(message="Plan name is required."),
        Length(min=2, max=50, message="Plan name must be between 2 and 50 characters.")
    ])
    duration_months = IntegerField('Duration (Months)', validators=[
        DataRequired(message="Duration is required."),
        NumberRange(min=1, max=120, message="Duration must be between 1 and 120 months.")
    ])
    price = DecimalField('Plan Price ($)', places=2, validators=[
        DataRequired(message="Price is required."),
        NumberRange(min=0.00, max=10000.00, message="Price must be between $0.00 and $10,000.00.")
    ])
    submit = SubmitField('Save Plan')
