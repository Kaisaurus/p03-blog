""" This is the main app file """
import webapp2

from handlers.bloghandler import BlogHandler
from handlers.login import Login, \
                           Logout
from handlers.signup import Register, \
                            Welcome
from handlers.postfunctions import NewPost, \
                                   PostPage, \
                                   EditPost, \
                                   DeletePost, \
                                   LikePost

from handlers.commentfunctions import NewComment, \
                                      EditComment, \
                                      DeleteComment

class BlogFront(BlogHandler):
    def get(self):
        posts = self.get_entries(100)
        self.render('front.html', posts=posts)

app = webapp2.WSGIApplication([('/', BlogFront),
                                 ('/welcome', Welcome),
                                 ('/blog/?', BlogFront),
                                 ('/blog/([0-9]+)', PostPage),
                                 ('/blog/newpost', NewPost),
                                 ('/blog/like', LikePost),
                                 ('/blog/delete', DeletePost),
                                 ('/blog/edit', EditPost),
                                 ('/blog/new_comment', NewComment),
                                 ('/blog/edit_comment', EditComment),
                                 ('/blog/delete_comment', DeleteComment),
                                 ('/signup', Register),
                                 ('/login', Login),
                                 ('/logout', Logout)
                                 ],
                                debug=True)