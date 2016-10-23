"""This module handles the login page"""

from handlers.bloghandler import BlogHandler
from models.user import User

# logs in
class Login(BlogHandler):
    # renders the login form
    def get(self):
        self.render('login-form.html')

    # logging in
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        # logs in using User class function if invalid returns None
        u = User.login(username, password)
        if u:
            # logs in using the function borrowed from BlogHandler
            self.login_cookie(u)
            self.redirect('/welcome')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)

# logs out
class Logout(BlogHandler):
    def get(self):
        # logs out using the function borrowed from BlogHandler
        self.logout()
        self.redirect('/')