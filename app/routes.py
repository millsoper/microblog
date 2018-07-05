from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
      {
        'author': {'username': 'werewolf'},
        'body': 'beautiful moon out tonight!'
      },
      {
        'author': {'username': 'vampire'},
        'body': 'heading out for drinks soon!'
      }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts) 

@app.route('/login')
def login():
  form = LoginForm()
  return render_template('login.html', title='Sign In', form=form)
