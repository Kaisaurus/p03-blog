import os
import re
import random
import hashlib
import hmac
import json
from string import letters

import webapp2
import jinja2

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                 autoescape = True)

secret = "Please_don't_steal_my_passwords"

def render_str_jinja(template, **params):
  t = jinja_env.get_template(template)
  return t.render(params)

def make_secure_val(val):
  return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
  val = secure_val.split('|')[0]
  if secure_val == make_secure_val(val):
    return val

##### user stuff
def make_salt(length = 5):
  return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
  if not salt:
    salt = make_salt()
  h = hashlib.sha256(name + pw + salt).hexdigest()
  return '%s|%s' % (salt, h)

def valid_pw(name, password, h):
  salt = h.split('|')[0]
  return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
  return ndb.Key('users', group)


class BlogHandler(webapp2.RequestHandler):
  def post(self):
    if not self.user:
      self.redirect('/')

  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    params['user'] = self.user
    return render_str_jinja(template, **params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

  def set_secure_cookie(self, name, val):
    cookie_val = make_secure_val(val)
    self.response.headers.add_header(
      'Set-Cookie',
      '%s=%s; Path=/' % (name, cookie_val))

  def read_secure_cookie(self, name):
    cookie_val = self.request.cookies.get(name)
    return cookie_val and check_secure_val(cookie_val)

  def login_cookie(self, user):
    self.set_secure_cookie('user_id', str(user.key.id()))

  def logout(self):
    self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

  def initialize(self, *a, **kw):
    webapp2.RequestHandler.initialize(self, *a, **kw)
    uid = self.read_secure_cookie('user_id')
    self.user = uid and User.by_id(int(uid))
    '''
    Gives self.user attribute to all classes that inherit from Bloghandler
    this is same as:
    if uid and User.by_id(int(uid)):
      self.user = uid
    '''

def render_post(response, post):
  response.out.write('<b>' + post.subject + '</b><br>')
  response.out.write(post.content)

class User(ndb.Model):
  name = ndb.StringProperty(required = True)
  pw_hash = ndb.StringProperty(required = True)
  created = ndb.DateTimeProperty(auto_now_add = True)
  likes = ndb.IntegerProperty(repeated=True)
  email = ndb.StringProperty()

  #decorator function allow you to call a function on a Class rather than an object of it
  @classmethod
  def by_id(cls, uid):
    return User.get_by_id(uid, parent = users_key())

  @classmethod
  def by_name(cls, name):
    return cls.query(cls.name == name).get()
    #u = User.all().filter('name =', name).get()
    #return u

  @classmethod
  def register(cls, name, pw, email = None):
    pw_hash = make_pw_hash(name, pw)
    return User(parent = users_key(),
          name = name,
          pw_hash = pw_hash,
          email = email)

  @classmethod
  def login(cls, name, pw):
    u = cls.by_name(name)
    if u and valid_pw(name, pw, u.pw_hash):
      return u

class Signup(BlogHandler):
  def get(self):
    #users = User.all().order('-created')
    users = User.query().order(-User.created)
    self.render("signup-form.html", users=users)


    '''
    e = Post.query()
    e = e.order(-Post.created)
    entries = e.fetch(n)
    return entries
    '''

  def post(self):
    have_error = False
    self.username = self.request.get('username')
    self.password = self.request.get('password')
    self.verify = self.request.get('verify')
    self.email = self.request.get('email')

    params = dict(username = self.username,
            email = self.email)

    if not valid_username(self.username):
      params['error_username'] = "That's not a valid username."
      have_error = True

    if not valid_password(self.password):
      params['error_password'] = "That wasn't a valid password."
      have_error = True
    elif self.password != self.verify:
      params['error_verify'] = "Your passwords didn't match."
      have_error = True

    if not valid_email(self.email):
      params['error_email'] = "That's not a valid email."
      have_error = True

    if have_error:
      self.render('signup-form.html', **params)
    else:
      self.done()

  def done(self, *a, **kw):
    raise NotImplementedError

class Register(Signup):
  def done(self):
    #make sure the user doesn't already exist
    u = User.by_name(self.username)
    if u:
      msg = 'That user already exists.'
      self.render('signup-form.html', error_username = msg)
    else:
      u = User.register(self.username, self.password, self.email)
      u.put()

      self.login_cookie(u)
      self.redirect('/welcome')

class Login(BlogHandler):
  def get(self):
    self.render('login-form.html')

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')

    u = User.login(username, password)
    if u:
      self.login_cookie(u)
      self.redirect('/welcome')
    else:
      msg = 'Invalid login'
      self.render('login-form.html', error = msg)

class Logout(BlogHandler):
  def get(self):
    self.logout()
    self.redirect('/')


class Welcome(BlogHandler):
  def get(self):
    if self.user:
      self.render('welcome.html')
    else:
      self.redirect('/signup')
'''
class Welcome(BlogHandler):
  def get(self):
    username = self.request.get('username')
    if valid_username(username):
      self.render('welcome.html', username = username)
    else:
      self.redirect('/signup')

'''

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
  return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
  return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
  return not email or EMAIL_RE.match(email)


##### blog stuff

def blog_key(name = 'default'):
  #return ndb.Key.from_path('blogs', name)
  return ndb.Key('blogs', name)

class Post(ndb.Model):
  subject = ndb.StringProperty(required = True)
  content = ndb.TextProperty(required = True)
  username = ndb.StringProperty(required=True)
  created = ndb.DateTimeProperty(auto_now_add = True)
  liked_by = ndb.IntegerProperty(repeated=True)
  last_modified = ndb.DateTimeProperty(auto_now = True)

  def render(self, current_user):
    self._render_text = self.content.replace('\n', '<br>')
    return render_str_jinja("post.html", p = self, current_user=current_user)

  def count_likes(self):
    return len(self.liked_by)

# get blog posts
  @classmethod
  def get_entries(cls, n=10):
    e = Post.query()
    e = e.order(-Post.created)
    entries = e.fetch(n)
    return entries

  @classmethod
  def by_name(cls, name):
    return cls.query(cls.username == name).fetch()

    #u = Post.all().filter('username =', name).get()
    #return u

  @classmethod
  def by_id(cls, post_id):
    return Post.get_by_id(post_id, parent=blog_key())

class BlogFront(BlogHandler):
  def get(self):
    posts = Post.get_entries(100)
    self.render('front.html', posts=posts)

class PostPage(BlogHandler):
  def get(self, post_id):
    #key = ndb.Key.from_path('Post', int(post_id), parent=blog_key())
    #post = ndb.get(key)
    #post = Post.get_by_id(int(post_id))
    post = Post.by_id(post_id)

    if not post:
      self.render('error.html', error="This post doesn't exist")
      #self.error(404)
      return

    self.render("permalink.html", post = post)

class NewPost(BlogHandler):
  def get(self):
    if self.user:
      user_posts = Post.by_name(self.user.name)

      self.render("newpost.html", user_posts=user_posts)
    else:
      self.redirect("/login")

  def post(self):
    if not self.user:
      self.redirect('/')

    subject = self.request.get('subject')
    content = self.request.get('content')
    username = self.user.name

    if subject and content:
      p = Post(parent = blog_key(), subject = subject, content = content, username = username)
      p.put()
      self.redirect('/blog/%s' % str(p.key.id()))
    else:
      error = "What kind of blog post doesn't have a subject and content? Get working!"
      self.render("newpost.html", subject=subject, content=content, error=error)

class LikePost(BlogHandler):
  def post(self):

    if not self.user:
      self.write(json.dumps(({'msg': 'error123'})))

    msg = "yo"
    self.write(json.dumps({'msg': msg}))
    post_id = int(self.request.get('post_id'))
    # retrieve post entity from datastore
    #post = Post.get_by_id(post_id)
    post = Post.by_id(post_id)
    # retrieve user id from initialise method
    user_id = self.user.key.id()
    user_name = self.user.name

    msg = post.likes
    self.write(json.dumps({'msg': msg}))
'''
    if user_name == post.username:
      error = "You can not add a  'like' to your own posts"
      self.write(json.dumps({'msg': error}))

    elif user_id in post.likes:
      error = "You can't like this twice"
      self.write(json.dumps({'msg': error}))

    else:
      post.likes.append(str(user_id))
      self.user.likes.append(post.key().id())
      self.write(json.dumps({'msg': post.count_likes()}))

      post.put()
      self.user.put()
'''
'''
    msg = post.username
    self.write(json.dumps({'msg': msg}))

      self.user.likes.remove(post.key.id())
      self.write(json.dumps(({'likes': post.likes, 'you-like': ''})))
      post.put()
      self.user.put()
    else:
      post.likes += 1
      post.liked_by.append(uid)
      self.user.likes.append(post.key.id())
      self.write(json.dumps(({'likes': post.likes, 'you-like': ' You like this'})))
      post.put()
      self.user.put()


    msg = "hey"+str(user_id+post_id)
    self.write(json.dumps({'msg': msg}))
'''




app = webapp2.WSGIApplication([('/', BlogFront),
                 ('/welcome', Welcome),
                 ('/blog/?', BlogFront),
                 ('/blog/([0-9]+)', PostPage),
                 ('/blog/newpost', NewPost),
                 ('/blog/like', LikePost),
                 ('/signup', Register),
                 ('/login', Login),
                 ('/logout', Logout)
                 ],
                debug=True)
