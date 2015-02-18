import hashlib
import uuid

from tests import  _execute_test

def create_user(username, password, first_name, \
        last_name, email, organization):

    success, payload = _execute_test(
        'admin/get_access_token.json',
        None,
        None,
        None,
        None,
        {
            'username': 'system',
            'password': hashlib.sha256('password').hexdigest(),
        },
        'POST',
    )
    token = payload['token'] 

    success, payload = _execute_test(
        'admin/create_user.json',
        token,
        None,
        None,
        None,
        {
            'user_type_id': 1,
            'client_id': str(uuid.uuid4()),
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name':  last_name,
            'email': email,
            'organization': organization,
            'fence_top_left_lat': 43.4,
            'fence_top_left_lng': -77.9,
            'fence_bottom_right_lat': 43.0,
            'fence_bottom_right_lng': -77.3,
        },
        'POST',
    )
    print 'New User ID: {0}'.format(payload['user_id'])


if __name__ == '__main__':

    create_user(
        username = "tduffy",
        password = hashlib.sha256('hhroc123%%%').hexdigest(),
        first_name = "Tim",
        last_name = "Duffy",
        email = "tim@timduffy.me",
        organization = "Hacks/Hackers Rochester",
    )

    create_user(
        username = "mbernius",
        password = hashlib.sha256('hhroc123%%%').hexdigest(),
        first_name = "Matt",
        last_name = "Bernius",
        email = "mbernius@gmail.com",
        organization = "Hacks/Hackers Rochester",
    )

    create_user(
        username = "mleonard",
        password = hashlib.sha256('wxxi123%%%').hexdigest(),
        first_name = "Matt",
        last_name = "Leonard",
        email = "mleonard@wxxi.org",
        organization = "WXXI",
    )

    create_user(
        username = "aruestow",
        password = hashlib.sha256('hhroc123%%%').hexdigest(),
        first_name = "Andy",
        last_name = "Ruestow",
        email = "andy@ruestow.me",
        organization = "Hacks/Hackers Rochester",
    )

    create_user(
        username = "mnolan",
        password = hashlib.sha256('hhroc123%%%').hexdigest(),
        first_name = "Mike",
        last_name = "Nolan",
        email = "me@michael-nolan.com",
        organization = "Hacks/Hackers Rochester",
    )

