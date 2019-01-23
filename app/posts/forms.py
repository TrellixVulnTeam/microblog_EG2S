from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app.models import User, Comment


class PostForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    category = SelectField('Your education level', choices = [('Music', 'Music'), ('Peoples Corner', 'Peoples Corner'), ('Travel', 'Travel'), ('Design', 'Design'), ('Sports', 'Sports'), ('Others', 'others..')])
    story_line = TextAreaField('Story Line', validators=[DataRequired()])
    story_text = TextAreaField('Story', validators=[DataRequired()])
    youtube_link= StringField('Youtube Link', validators=[DataRequired()])

    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])

    submit = SubmitField('Submit')
