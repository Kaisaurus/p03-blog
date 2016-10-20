"""This module is for the Post model"""

from models.comment import Comment

from google.appengine.ext import ndb
from handlers import helpers

class Post(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    username = ndb.StringProperty(required=True)
    liked_by = ndb.StringProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    # creates a function to render text in html replacing line breaks with <br> tags
    def render(self, current_user):
        self._render_text = self.content.replace('\n', '<br>')
        self.comments = Comment.by_post_id(int(self.key.id()))
        return helpers.render_str_jinja("post.html", p=self, current_user=current_user,comments=self.comments)

    def count_likes(self):
        return len(self.liked_by)

    def render_comment(self, comment_id, current_user):
        return Comment.get_by_id(int(comment_id)).render(current_user)

    @classmethod
    def by_name(cls, name):
        return cls.query(cls.username == name).fetch()

    @classmethod
    def by_id(cls, post_id):
        return cls.get_by_id(int(post_id))
