from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class EditProfileForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
  submit = SubmitField('Submit')

  def __init__(self, original_username, *args, **kwargs):
    super(EditProfileForm, self).__init__(*args, **kwargs)
    self.original_username = original_username

  def validate_username(self, username):
    if username.data != self.original_username:
      user = User.query.filter_by(username=self.username.data).first()
      if user is not None:
        raise ValidationError('Please use a different username.')

class EditPostForm(FlaskForm):
  body = TextAreaField('Body', validators=[DataRequired(), Length(min=1, max=420)])
  month = SelectField('Month', choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], coerce=int)
  date = SelectField('Day', choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12), (13,13), (14,14), (15,15), (16,16), (17,17), (18,18), (19,19), (20,20), (21,21), (22,22), (23,23), (24,24), (25,25), (26,26), (27,27), (28,28), (29,29), (30,30), (31,31)], coerce=int)
  submit = SubmitField('Submit')

  def __init__(self, original_body, *args, **kwargs):
    super(EditPostForm, self).__init__(*args, **kwargs)
    self.original_body = original_body

class PostForm(FlaskForm):
  post = TextAreaField('Say something', validators=[
    DataRequired(), Length(min=1, max=420)])
  submit=SubmitField('Submit')

class ResetPasswordRequestForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Request Password Reset')
