from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, g
from flask_login import current_user, login_required
from app.models import User, Post
from app import db
from app.main.forms import EditProfileForm, PostForm, EditPostForm, SearchForm
from app.main import bp

@bp.before_app_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()
  g.search_form = SearchForm()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    posts =  Post.query.order_by(Post.timestamp.desc()).paginate(
    page, current_app.config['POSTS_PER_PAGE'], False) 
    next_url = url_for('main.index', page=posts.next_num) \
      if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
      if posts.has_prev else None
    return render_template('index.html', title='home', posts=posts.items,
                            next_url=next_url, prev_url=prev_url) 

@bp.route('/search')
def search():
    if not g.search_form.validate():
      return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts, total =  Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
      if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
      if page > 1 else None
    return render_template('search.html', title='search', posts=posts, next_url=next_url, prev_url=prev_url)

@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
      post = Post(body=form.body.data, author=current_user, title=form.title.data)
      db.session.add(post)
      db.session.commit()
      flash('Your post is now live!')
      return redirect(url_for('main.index'))
    return render_template('create_post.html', title='create', 
                            form=form) 

@bp.route('/delete_post')
def delete_post():
  postId = request.args.get('postId')
  Post.query.filter(Post.id == postId).delete()
  db.session.commit()
  return redirect(url_for('main.index'))

@bp.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  posts = user.posts.order_by(Post.timestamp.desc()).paginate(
    page, current_app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('main.user', username=user.username, page=posts.next_num) \
    if posts.has_next else None
  prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
    if posts.has_prev else None 
  return render_template('user.html', user=user, posts=posts.items, 
                        next_url=next_url, prev_url=prev_url)

@bp.route('/about')
def about():
  return render_template('about.html', title='about')

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm(current_user.username)
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title='Edit Profile',
                         form=form)

@bp.route('/edit_post', methods=['GET', 'POST'])
@login_required
def edit_post():
  postId = request.args.get('postId')
  givenPost = Post.query.filter_by(id=postId).first()
  oldDate = datetime.strptime(str(givenPost.timestamp), "%Y-%m-%d %H:%M:%S.%f")
  form = EditPostForm(givenPost.body)
  if form.validate_on_submit():
    if givenPost:
      newDate = oldDate.replace(day=form.date.data, month=form.month.data)
      givenPost.body = form.body.data
      givenPost.title = form.title.data
      givenPost.timestamp = newDate
      db.session.commit()
      flash('Your changes have been saved.')
  elif request.method == 'GET':
    form.body.data = givenPost.body 
    form.date.data = oldDate.day
    form.title.data = givenPost.title
    form.month.data = oldDate.month
  return render_template('edit_post.html', title='Edit Post', form=form)
