"""
I hope I come up with a better name for this
"""
import api_vars
from bson.objectid import ObjectId


def prepare_statements(model, incoming):
    """

    Parameters
    ----------
    model : dict
    incoming : dict

    Returns
    -------
    dict
    """
    outgoing = {}
    for model_key, is_required in model.items():
        value = incoming.get(model_key)
        if value is None and is_required:
            print(model_key, "not there")
            return {"error": model_key + " is required"}
        elif value is not None:
            outgoing[model_key] = value
    return outgoing


def user_grab(user_id):
    user = api_vars.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        return None
    user['_id'] = str(user['_id'])
    return user


def add_post_to_user(user_id, post_id):
    try:
        user = user_grab(user_id)
    except:
        return
    # silently fail for now
    if user is None:
        return
    shared_posts = user.get("shared_posts")
    # add the post to the user list
    if shared_posts is None:
        shared_posts = []
    print(shared_posts)
    api_vars.users.update({'_id': ObjectId(user_id)},
                          {"$set": {'shared_posts': shared_posts}})