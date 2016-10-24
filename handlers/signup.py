'''This module handles user signup'''

from handlers.bloghandler import BlogHandler
from handlers import helpers
from models.user import User


# signup page handler


class Signup(BlogHandler):

    def get(self):
        users = User.query().order(-User.created)
        self.render("signup-form.html", users=users)

    def post(self):
        # set variables for error and data received from html form
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        # save the username and email in parameters so these inputs dont reset
        # when an error occurs.
        params = dict(username=self.username,
                      email=self.email)

        if not helpers.valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not helpers.valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not helpers.valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self):
        '''This is just a placeholder which does not get called'''
        raise NotImplementedError


# this handles the actual registration***


class Register(Signup):

    '''This class handles the registration after validation'''

    def done(self):
        # This done method overrides the done() from Signup
        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()
            self.login_cookie(u)
            self.redirect('/welcome')


# This handles the welcome page


class Welcome(BlogHandler):
    # render welcome page when singup is successful, if the cookie isnt set
    # correctly it redirects to the signup page

    def get(self):
        if self.user:
            self.render('welcome.html')
        else:
            helpers.error_page(self, 'Login failed')
