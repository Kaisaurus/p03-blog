# Model for comments

from google.appengine.ext import ndb
from handlers import helpers

class Comment(ndb.Model):
    # Comment properties
    post_id = ndb.IntegerProperty()
    user_name = ndb.StringProperty(required=True)
    comment = ndb.TextProperty(required=True)
    liked_by = ndb.IntegerProperty(repeated=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    # render a comment using the comment.html template
    def render(self, user_name):
        self._render_text = self.comment.replace('\n', '<br>')
        # the current user name and the comment is passed to the template
        return helpers.render_str_jinja("comment.html", c=self, user_name=user_name)

    # returns all comments by post_id of the post they belong to
    @classmethod
    def by_post_id(cls, post_id):
        return cls.query(cls.post_id==int(post_id)).fetch()