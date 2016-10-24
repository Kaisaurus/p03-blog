"""This module handles all post functionality """
import datetime
import json

from google.appengine.ext import ndb
from models.post import Post
from models.comment import Comment
from handlers.bloghandler import BlogHandler
from handlers import helpers


class PostPage(BlogHandler):

    def get(self, post_id):
        post = Post.by_id(post_id)

        if post:
            self.render("permalink.html", post=post)
        else:
            error = "Could not retrieve requested post"
            helpers.error_page(self, error=error)


class NewPost(BlogHandler):

    def get(self):
        if self.user:
            user_posts = Post.by_name(self.user.name)
            self.render("newpost.html", user_posts=user_posts)
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            error = "Looks like something went wrong, that action is not all" \
                    "owed when not logged in."
            error_page(self, error=error)
            return

        subject = self.request.get('subject')
        content = self.request.get('content')
        user_name = self.user.name

        if subject and content:
            p = Post(subject=subject, content=content, user_name=user_name)
            p.put()
            self.redirect('/blog/%s' % str(p.key.id()))
        else:
            error = "What kind of blog post doesn't have a subject and conte" \
                    "nt? Get working!"
            self.render(
                "newpost.html", subject=subject, content=content, error=error)


class LikePost(BlogHandler):

    def post(self):
        if not self.user:
            self.write(
                json.dumps({'msg': "You must be logged in to 'Like' a post."}))

        post = Post.by_id(self.request.get('post_id'))

        if self.user.name == post.user_name:
            # this shouldn't ever happen since the button shouldn't appear for
            # same user posts. But just in case someone tries something funny..
            self.write(json.dumps({'msg': 'You cannot like your own post.'}))
        else:
            # retrieve user name
            user_name = self.user.name

            if user_name in post.liked_by:
                post.liked_by.remove(user_name)
                self.user.likes.remove(post.key.id())
                self.write(
                    json.dumps({'like_btn_txt': 'Like',
                                'likes_counter': post.count_likes()}))

            else:
                post.liked_by.append(user_name)
                self.user.likes.append(int(post.key.id()))
                self.write(
                    json.dumps({'likes_counter': post.count_likes(),
                                'like_btn_txt': 'Unlike'}))

            post.put()
            self.user.put()


class DeletePost(BlogHandler):

    def post(self):
        post_id = self.request.get('post_id')
        post = Post.by_id(post_id)
        comments = Comment.by_post_id(post_id)

        if self.user.name == post.user_name:
            if comments:
                for c in comments:
                    c.key.delete()
            post.key.delete()
            self.write(json.dumps({'msg': 'success'}))
        else:
            self.write(
                json.dumps({'msg': "You are not allowed to delete someone el"
                                   "se's post"}))


class EditPost(BlogHandler):

    def post(self):
        post = Post.by_id(self.request.get('post_id'))

        if self.user.name == post.user_name:
            post.subject = self.request.get('post_subject')
            post.content = self.request.get('post_content')
            post.last_modified = datetime.datetime.now()
            post.put()
            self.write(
                json.dumps({'datetime': post.last_modified
                                            .strftime("%b %d, %Y - %H:%M")}))
        else:
            self.write(
                json.dumps({'msg': "You are not allowed to delete someone el"
                                   "se's post"}))
