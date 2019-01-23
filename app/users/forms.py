from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User, Address, Occupation, Links, Intrest, Achievement, Events, Travel, Special_event, Media, Language, Sponsership





class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    about_me = StringField('About you', validators=[DataRequired()])
    gender = RadioField('Gender', choices = [('Male','Male'),('Female','Female')], validators=[DataRequired()])
    contact_number = IntegerField("phone number", validators=[DataRequired()])
    education_level = SelectField('Your education level', choices = [('High school', 'High School'), ('Under Graduation', 'Under Graduation'), ('Post Graduation', 'Post Graduation'), ('Diploma', 'Diploma'), ('Ph.D', 'Ph.D')])
    date_of_birth = DateField('date of birth', format="%Y-%m-%d")
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != User.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_username(self, email):
        if email.data != User.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')






class AddressForm(FlaskForm):
    street = StringField('Street Address')
    city = StringField('City')
    zip_code = StringField('Zip Code')
    country = SelectField('Country', choices = [('India', 'India'), ('Netherlands', 'Netherlands'), ('USA', 'USA'), ('United Kingdom', 'United Kingdom')])
    submit = SubmitField('Update')

class OccupationForm(FlaskForm):
    occupation_name = StringField('occupation name')
    occupation_company = StringField(' occupation company ')
    occupation_start_date = DateField('Start Date', format="%Y-%m-%d")
    occupation_end_date = DateField('End Date', format="%Y-%m-%d")
    submit = SubmitField('Update')


class LinksForm(FlaskForm):
    facebook_id = StringField('link Facebook')
    twitter_id = StringField('Link Twitter')
    instagram_id = StringField(' Link Instagram ')
    snapchat_id = StringField(' Link Snapchat ')
    submit = SubmitField('Update')

class IntrestForm(FlaskForm):
    intrest_type = StringField('Intrest name')
    submit = SubmitField('Update')

class AchievementForm(FlaskForm):
    medal_count = StringField('medal')
    timestamp = DateField(' Date', format="%Y-%m-%d")
    submit = SubmitField('Update')

class EventsForm(FlaskForm):
    event_name = StringField('Event Name')
    event_description = StringField('Event description')
    event_location = StringField('location')
    event_start_date = DateField(' Start Date', format="%Y-%m-%d")
    event_end_date = DateField(' End Date', format="%Y-%m-%d")
    event_status = BooleanField('Event Status')
    submit = SubmitField('Update')

class TravelForm(FlaskForm):
    place = StringField('location')
    start_date = DateField(' Start Date', format="%Y-%m-%d")
    end_date = DateField(' End Date', format="%Y-%m-%d")
    submit = SubmitField('Update')

class Special_eventForm(FlaskForm):
    life_event = StringField('Discription')
    life_event_start_date = DateField(' Start Date', format="%Y-%m-%d")
    life_event_end_date = DateField(' End Date', format="%Y-%m-%d")
    submit = SubmitField('Update')

class MediaForm(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    media_format = SelectField('Media type ', choices = [('image', 'image')])
    submit = SubmitField('upload')

class LanguageForm(FlaskForm):
    language = StringField('language')
    language_accuracy = SelectField('Accuracy', choices = [('A', 'excellent'), ('B', 'Good'), ('C', 'Average'), ('D', 'Poor')])
    submit = SubmitField('Update')

class SponsershipForm(FlaskForm):
    sponser_type =  SelectField('Sponser Type', choices = [('INDV', 'Individual'), ('BRAND', 'Brand'), ('PROUDH', 'Production House'), ('WELFARE', 'Welfare Community')])
    sponser_name = StringField('Sponser Name')
    sponsership_start_date = DateField(' Start Date', format="%Y-%m-%d")
    sponsership_end_date = DateField(' End Date', format="%Y-%m-%d")
    submit = SubmitField('Update')
