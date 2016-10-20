# Model for comments

from google.appengine.ext import ndb
from handlers import helpers

class Comment(ndb.Model):
    post_id = ndb.IntegerProperty()
    user_name = ndb.IntegerProperty(required=True)
    comment = ndb.TextProperty(required=True)
    liked_by = ndb.IntegerProperty(repeated=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    def render(self, current_user):
        self._render_text = self.comment.replace('\n', '<br>')
        return helpers.render_str_jinja("comment.html", c=self, username=self.user_name , current_user=current_user)

    def count_likes(self):
        #returns like count
        return len(self.liked_by)

    @classmethod
    def by_post_id(cls, post_id):
        return cls.query(cls.post_id == post_id).fetch()