"""This module handles  all comments functionality"""

import json

from google.appengine.ext import ndb
from models.comment import Comment
from handlers.bloghandler import BlogHandler

# Creates a new comment


class NewComment(BlogHandler):

    def post(self):
        if not self.user:
            self.write(
                json.dumps({'msg': "You must be logged in to 'Comment' on a post."}))
            return

        post_id = int(self.request.get('post_id'))
        comment = self.request.get('comment')
        user_name = self.user.name

        if comment:
            # creates a comment entry if it isn't empty
            c = Comment(post_id=post_id, user_name=user_name, comment=comment)
            c.put()
            comment_html = c.render(user_name)
            self.write(json.dumps({'comment': comment_html}))
        else:
            self.write(json.dumps({'msg': "A comment cannot be empty."}))
            return

# Deletes a comment


class DeleteComment(BlogHandler):

    def post(self):
        comment = Comment.get_by_id(int(self.request.get('comment_id')))

        # check if logged in user corresponds to comment user
        if self.user.name == comment.user_name:
            # deletes the comment entry with the corresponding id
            comment.key.delete()
            self.write(json.dumps({'msg': 'success'}))
        else:
            self.write(
                json.dumps({'msg': "You are not allowed to delete someone else's comment"}))


class EditComment(BlogHandler):
    # Edits a comment

    def post(self):
        comment = Comment.get_by_id(int(self.request.get('comment_id')))

        # check if logged in user corresponds to comment user
        if self.user.name == comment.user_name:
            # changes the comment to the newly posted comment and returns the
            # date it modified
            comment.comment = self.request.get('content_new')
            comment.put()
            self.write(
                json.dumps({'datetime': comment.last_modified.strftime("%b %d, %Y - %H:%M")}))
        else:
            self.write(
                json.dumps({'msg': "You are not allowed to edit someone else's comment"}))
