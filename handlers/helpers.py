"""This module provides global helper functions"""
import os
import jinja2
import re
import hmac
import random
import string
import hashlib

from google.appengine.ext import ndb
from handlers.secret import SECRET

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

# Regular expressions to verify input
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

# Helper functions to verify input useing the above regular expressions
def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

# renders a jinja template using the received parameters
def render_str_jinja(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# makes a secure val using Secret and hmac hashing
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(SECRET, val).hexdigest())

# checks if val is secure by recreating secure van and comparing it
def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

# creates a random new salt
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))

# creates a password hash using sha 256
def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (salt, h)

# checks if password is valid by trying to recreate it using make_pw_hash
def valid_pw(name, password, h):
    salt = h.split('|')[0]
    return h == make_pw_hash(name, password, salt)

# TO BE DELETED
def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

# renders the error page with a given error
def error_page(handler, error):
    handler.render('error.html', error=error)

# key for users database (groups can be used for future functionality)
def users_key(group = 'default'):
    return ndb.Key('users', group)