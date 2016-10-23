"""This module is for the Post model"""

from models.comment import Comment

from google.appengine.ext import ndb
from handlers import helpers

class Post(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    user_name = ndb.StringProperty(required=True)
    liked_by = ndb.StringProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now_add=True)

    # creates a function to render text in html replacing line breaks with <br> tags
    def render(self, user_name):
        self._render_text = self.content.replace('\n', '<br>')
        self.comments = Comment.by_post_id(self.key.id())
        return helpers.render_str_jinja("post.html", p=self, user_name=user_name, comments=self.comments)

    # return the amount of likes the post has received
    def count_likes(self):
        return len(self.liked_by)

    @classmethod
    def by_name(cls, name):
        return cls.query(cls.user_name == name).fetch()

    @classmethod
    def by_id(cls, post_id):
        return cls.get_by_id(int(post_id))
