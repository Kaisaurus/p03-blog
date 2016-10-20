'''This module is the general blog handler '''

import webapp2

from handlers import helpers
from models.user import User
from models.post import Post

class BlogHandler(webapp2.RequestHandler):
    # general write function taking parameters
    def write(self, *a, **params):
        self.response.out.write(*a, **params)

    # TO BE DELETED
    def render_str(self, template, **params):
        params['user'] = self.user.name
        return helpers.render_str_jinja(template, **params)

    # render a page using jinja and passing the current user as 'user' param so it is avialable in all templates
    def render(self, template, **params):
        params['user'] = self.user.name
        self.write(helpers.render_str_jinja(template, **params))

    # general function to set a secure cookie
    def set_secure_cookie(self, name, val):
        # this uses the helper function to create the secure cookie
        cookie_val = helpers.make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    # reads cookie and checks if it is secure (see helper function for details)
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and helpers.check_secure_val(cookie_val)

    # sets user_id cookie using the set_secure_cookie function
    def login_cookie(self, user):
        self.set_secure_cookie('user_id', str(user.key.id()))

    # empty login cookie
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    # get blog posts
    def get_entries(self, n=10):
        e = Post.query()
        e = e.order(-Post.created)
        entries = e.fetch(n)
        return entries

    #init function is run when initialising the app
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        # if the user is set, makes it available to all children Classes by assigning it to attribute user
        self.user = uid and User.by_id(int(uid))
