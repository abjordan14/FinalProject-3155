from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectMultipleField, HiddenField
from wtforms.validators import Length, DataRequired, EqualTo, Email, InputRequired
from wtforms import ValidationError
from .models import User
from .database import db

class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    firstname = StringField('First Name', validators=[Length(1,10)])
    lastname = StringField('Last Name', validators=[Length(1,10)])
    email = StringField('Email', [Email(message='Not a valid email address!'),
                                  DataRequired()
                                  ])
    password = PasswordField('Password', [DataRequired(message='Please enter a password.'),
                                          EqualTo('confirmPassword', message='Passwords must match'
                                                  )])
    confirmPassword = PasswordField('Confirm Password', validators=[Length(min=6, max=10)])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Username already exists!')

class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    email = StringField('Email', [Email(message='Not a valid email address'), DataRequired()])
    password = PasswordField('Password', [DataRequired(message='Please enter a password.')])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect login credentials')

class CommentForm(FlaskForm):
    class Meta:
        csrf = False
    comment = TextAreaField('Comment', validators=[Length(min=1)])
    submit = SubmitField('Add Comment')

class RatingForm(FlaskForm):
    rating = HiddenField('rating', validators=[InputRequired()])
    
 #search
class SearchForm(Form):
  search = StringField('search', [DataRequired()])
  submit = SubmitField('Search', render_kw={'class': 'btn btn-success btn-block'})
