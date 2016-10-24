# Model for comments

from google.appengine.ext import ndb
from handlers import helpers


class Comment(ndb.Model):

    """
    Comment:
        a comment to a post
    Args:
        post_id     (int): id of the post the comment is directed to
        user_name   (str): name of the user commenting
        comment     (str): content of the comment
        liked_by    (str): list of user names the comment is liked by (for futre use)
        last_modified(dt): DateTime that the comment is last modified on
    Returns:
        A Comment ndb.Model
    """
    post_id = ndb.IntegerProperty()
    user_name = ndb.StringProperty(required=True)
    comment = ndb.TextProperty(required=True)
    liked_by = ndb.StringProperty(repeated=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    # render a comment using the comment.html template
    def render(self, user_name):
        self._render_text = self.comment.replace('\n', '<br>')
        # the current user name and the comment is passed to the template
        return helpers.render_str_jinja("comment.html",
                                        c=self,
                                        user_name=user_name)

    # returns all comments by post_id of the post they belong to
    @classmethod
    def by_post_id(cls, post_id):
        return cls.query(cls.post_id == int(post_id)).fetch()
