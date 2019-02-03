from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from app.models import User, Comment
# Grabbing CKEditorField as a rich-text-editor support
from flask_ckeditor import CKEditorField


class BlogForm(FlaskForm):
    blog_city = StringField('City', validators=[DataRequired()])
    blog_category = SelectField('Choose your blog subject', choices = [('Music', 'Music'), ('Peoples Corner', 'Peoples Corner'),
                          ('Travel', 'Travel'), ('Design', 'Design'), ('Sports', 'Sports'),('Arts', 'Arts'),
                          ('Health and Fitness', 'Health and Fitness'),('Wellness and Beauty', 'Wellness and Beauty'),
                          ('Food and Drink', 'Food and Drink'), ('Writing', 'Writing'),('Language and Culture', 'Language and Culture'),
                          ('Social and Political Movements', 'Social and Political Movements'),('Film', 'Film'),('Games and Sci-Fi', 'Games and Sci-Fi'),('Beliefs', 'Beliefs'),
                          ('Dance', 'Dance'),('Singing', 'Singing'),('Hobbies and Crafts', 'Hobbies and Crafts'), ('Family and Social', 'Family and Social'),('Career and Business', 'Career and Business'),
                          ('Adventure Sports', 'Adventure Sports'),('Science and Technology', 'Science and Technology'),
                          ('Others', 'others..')])
    blog_story_line = TextAreaField('Blog Headline', validators=[DataRequired()])
    blog_story_text = CKEditorField('Blog Text', validators=[DataRequired()])
    blog_youtube_link= StringField('Youtube Link', validators=[DataRequired()])
    blog_picture = FileField('Add Blog Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Blog Post')

class BlogCommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])

    submit = SubmitField('Submit')
