from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

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
  title = StringField('Title', validators=[DataRequired()])
  body = TextAreaField('Body', validators=[DataRequired(), Length(min=1, max=420)])
  month = SelectField('Month', choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')], coerce=int)
  date = SelectField('Day', choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10), (11,11), (12,12), (13,13), (14,14), (15,15), (16,16), (17,17), (18,18), (19,19), (20,20), (21,21), (22,22), (23,23), (24,24), (25,25), (26,26), (27,27), (28,28), (29,29), (30,30), (31,31)], coerce=int)
  submit = SubmitField('Submit')

  def __init__(self, original_body, *args, **kwargs):
    super(EditPostForm, self).__init__(*args, **kwargs)
    self.original_body = original_body

class PostForm(FlaskForm):
  body = TextAreaField('Say something', validators=[
    DataRequired(), Length(min=1, max=420)])
  title = StringField('Title', validators=[DataRequired()])
  submit=SubmitField('Submit')
