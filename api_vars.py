"""
Has variables that we want to treat as global
"""
from pymongo import MongoClient

# uses the default MongoDB client
client = MongoClient()
db = client.video_db
users = db.users
posts = users.posts
responses = posts.responses

# Values indicate whether they are required (True) or not (False)
# Uses dictionaries as a quick coding solution, but there are possible
# pitfalls, i.e. the dict is mutable, no type checks
USER_MODEL = {"name": True, "email": True, "age": False, "birthday": False,
              "public": True}
POST_MODEL = {'creator': True, 'message': True, 'links': False, 'images': False,
              'user_likes': False, 'friends': True}

