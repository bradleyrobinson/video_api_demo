"""
By Bradley Robinson

This is created for the purpose of a class project in the Masters in Data
Science at Southern Methodist University, and is provided AS IS with no
warranties.

This is an API that could, in theory be used by web, android or iOS. It is a
simple video sharing type website that pretends to send videos.

Things that are NOT implemented:

- authentication (pretends that everyone is already authenticated.
- video streaming
- rigorous unit testing
- ANY SEMBLANCE OF SECURITY NOTHING IS SECURE THE CTHULU WILL HAUNT YOU IF YOU
TRY TO USE THIS ON ANY PUBLICLY AVAILABLE SERVER

What it DOES (or will) have:
- A workable API that allows you to:
    - create a basic profile
    - share a video with selected friends
    - request friendships
    -
"""
from flask import Flask, request
from common import prepare_statements, user_grab, add_post_to_user
from bson.objectid import ObjectId
import api_vars
import json

app = Flask(__name__)


@app.route("/user", methods = ['POST'])
def user():
    """
    Allows someone to create a user

    Returns
    -------

    """
    incoming_user = request.json
    if incoming_user is None:
        return "no user json", 404
    incoming_email = incoming_user.get("email")
    if incoming_email is not None:
        try:
            user = api_vars.users.find_one({"email": incoming_email})
            if user is not None:
                return "bad request", 404
        except:
            pass
    prepared_user = prepare_statements(api_vars.USER_MODEL, incoming_user)
    error = prepared_user.get("error")
    if error is not None:
        return error
    prepared_user['_id'] = str(api_vars.users.insert_one(prepared_user).inserted_id)
    json_data = json.dumps(prepared_user)
    return json_data


@app.route("/user/<user_id>", methods = ['GET', 'PUT'])
def get_user(user_id):
    user = user_grab(user_id)
    return json.dumps(user)


@app.route("/users", methods = ['GET'])
def get_possible_friends():
    """
    Finds people that could be friends
    Returns
    -------

    """
    user_list = []
    for user_unprocessed in api_vars.users.find({'public': True}):
        user = user_unprocessed
        user['_id'] = str(user['_id'])
        user_list.append(user)
        # For now, let's break the list at one hundred. This is just for the
        # sake of simplicity.
        if len(user_list) >= 100:
            break
    user_data = {'users': user_list}
    json_data = json.dumps(user_data)
    return json_data


@app.route("/user/<user_id>/friend/<friend_id>", methods = ['GET', 'PUT'])
def make_friend(user_id, friend_id):
    """
    Make a new friend! Or get their information

    Parameters
    ----------
    user_id
    friend_id

    Returns
    -------

    """
    # Find out if the user exists
    user_a = user_grab(user_id)
    if user_a is None:
        return "user not found", 404

    # Find the other user
    user_b = user_grab(friend_id)
    if user_b is None:
        return "user not found", 404

    # Get their friend list
    friends_current = user_a.get("friends")
    friends_updated = []
    if friends_current is not None:
        for friend in friends_current:
            if friend == friend_id:
                return user_b
        friends_updated = friends_current
    friends_updated.append(str(user_b['_id']))
    api_vars.users.update({'_id': ObjectId(user_id)},
                          {'$set': {'friends': friends_updated}})
    return json.dumps(user_b)


@app.route("/user/<user_id>/friends", methods = ['GET'])
def friends(user_id):
    """ Simply allows one to get what friends they have

    Parameters
    ----------
    user_id : str

    Returns
    -------
    A json of friends, names and their ids
    """
    user = user_grab(user_id)
    if user is None:
        return "user not found", 404
    friends = user.get("friends")
    if friends is None:
        friends = []
    data_json = json.dumps({'friends': [str(friend) for friend in friends]})
    return data_json


@app.route("/user/<user_id>/feed")
def get_feed(user_id):
    user = user_grab(user_id)
    posts = user.get("shared_posts")
    if posts is None:
        posts = []
    extracted_posts = []
    for id in posts:
        post = api_vars.posts.find_one({"_id": ObjectId(id)})
        if post is not None:
            post['_id'] = str(post['_id'])
            extracted_posts.append(post)
    posts_json = json.dumps({'posts:': extracted_posts})
    return posts_json


@app.route("/user/<user_id>/share", methods=['POST'])
def share(user_id):
    incoming_post = request.json
    if incoming_post is None:
        return "no post", 400

    user = user_grab(user_id)
    if user is None:
        return "no user", 404

    incoming_user_id = incoming_post.get("creator")
    if incoming_user_id is None or incoming_user_id != user_id:
        incoming_post['creator'] = user_id
    prepared_post = prepare_statements(api_vars.POST_MODEL, incoming_post)

    error = prepared_post.get("error")
    if error is not None:
        return prepared_post, 400
        # add the value to each user

    post_id = api_vars.posts.insert_one(prepared_post).inserted_id
    for u in prepared_post['friends']:
        add_post_to_user(u, post_id)
    prepared_post['_id'] = str(post_id)
    json_post = json.dumps(prepared_post)
    return json_post


@app.route("/")
def home():
    """
    The main page. Since this is a demo, this just demonstrates things are on

    In a normal app, this may be used to check a login or something along those
    lines (though a login route may be possible too)

    Returns
    -------
    "Hello World!"
    """
    return "hello, world"


if __name__ == '__main__':
    # Only used when running locally for development. Don't run directly on a
    # server
    app.run(port=5000, debug=True)
