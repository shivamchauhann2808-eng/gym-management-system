from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, Regexp
from datetime import date

class MemberForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(message="Full name is required."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])
    profile_photo = FileField('Profile Photo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Only images are allowed!')
    ])
    gender = SelectField('Gender', choices=[
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ], validators=[DataRequired(message="Please select a gender.")])
    
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[
        DataRequired(message="Date of birth is required.")
    ])
    phone = StringField('Phone Number', validators=[
        DataRequired(message="Phone number is required."),
        Regexp(r'^\+?[0-9\s\-()]{7,20}$', message="Please enter a valid phone number.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Please enter a valid email address."),
        Length(max=120)
    ])
    address = TextAreaField('Residential Address', validators=[
        Optional(),
        Length(max=500, message="Address must be under 500 characters.")
    ])
    
    plan_id = SelectField('Membership Plan', coerce=int, validators=[
        DataRequired(message="Please select a membership plan.")
    ])
    join_date = DateField('Join Date', format='%Y-%m-%d', default=date.today, validators=[
        DataRequired(message="Join date is required.")
    ])
    status = SelectField('Membership Status', choices=[
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Pending', 'Pending')
    ], default='Active', validators=[DataRequired(message="Please select status.")])
    
    password = PasswordField('Login Password', validators=[
        Optional(),
        Length(min=6, message="Password must be at least 6 characters.")
    ])
    
    submit = SubmitField('Save Member')
