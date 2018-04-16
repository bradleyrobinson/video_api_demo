"""
By Bradley Robinson

This will allow a user to test out the system

"""
import requests
import json
import random
url = 'http://127.0.0.1:5000/user'


def create_user(name, email, age, public=True):
    user = {'name': name, 'email': email, 'age': age, 'public': public}
    resp = requests.post(url, json=user)
    if resp.status_code == 200 and resp.content is not None:
        data = json.loads(resp.content)
        return data.get('_id')
    return


def make_friend(user1, user2):
    my_url = url + '/' + user1 + '/friend/' + user2
    resp = requests.get(my_url)
    if resp.status_code == 200:
        return True
    return False


def share(user_id, share_ids, message):
    my_url = url + '/' + user_id + '/share'
    data = {'message': message, 'creator': user_id, 'friends': share_ids}
    resp = requests.post(my_url, json=data)
    if resp.status_code == 200:
        data = json.loads(resp.content)
        return data.get('_id')
    return


if __name__ == '__main__':
    users = []
    names = ['bob', 'sally', 'fred', 'scarlett', 'jack', 'dylan', 'johnny',
             'john', 'aaron', 'erin', 'prince', 'jimi', 'janelle', 'kendrick',
             'barack', 'henry', 'harry', 'ron', 'hermione', 'george', 'molly',
             'pikachu', 'ash', 'zack', 'bill', 'washington', 'donald', 'larry',
             'leonard', 'michelangelo', 'ty', 'dj', 'jt', 'billy-bob',
             'charmander', 't-rex', 'chicken', 'stewart', 'braxton', 'mustard',
             'green', 'white', 'plum', 'maid', 'mark', 'jeff', 'jeffrey',
             'shrimp']
    for i in range(20):
        for name in names:
            new_name = name + ' ' + names[random.randint(0, len(names)-1)]
            id = create_user(new_name, name + str(random.randint(0, 1000000)) +
                             '@gmail', random.randrange(13, 99))
            if id is not None:
                users.append(id)
    id_and_friends = {}
    for id in users:
        new_users = users.copy()
        random.shuffle(new_users)
        new_friends = new_users[0:20]
        for new_friend in new_friends:
            make_friend(id, new_friend)
        id_and_friends[id] = new_friends
    share_ids = []
    for id, friends in id_and_friends.items():
        id = share(id, friends,
                   "hello to " + names[random.randint(0, len(names)-1)])
        if id is not None:
            share_ids.append(id)
    print(share_ids)
