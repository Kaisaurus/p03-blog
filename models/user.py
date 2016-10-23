from google.appengine.ext import ndb
from handlers import helpers

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    likes = ndb.IntegerProperty(repeated=True)
    email = ndb.StringProperty()

    @classmethod
    def by_name(cls, name):
        return cls.query(cls.name == name).get()

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = helpers.make_pw_hash(name, pw)
        return User(name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and helpers.valid_pw(name, pw, u.pw_hash):
            return u
