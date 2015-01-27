
import uuid
import json
import requests
import datetime
import hashlib

ROOT_DOMAIN = "http://127.0.0.1:5002/"

def log(output):

    print "[{0}]: {1}".format(str(datetime.datetime.now()).split('.')[0],output)

def url_action(url_payload, data, method, files=None):

    """
        url_action(url, data, method)

            url = url to send
            data = dict of things to send
            method = 'GET' or 'POST'

    """

    json_response = None
    if True:
    #try:

        if method == 'GET':

            #url_payload = url_payload + "?"

            for key, value in data.items():
                url_payload += "{0}={1}&".format(key,value)

            log("URL: {0}".format(url_payload))

            http_response = requests.get(url_payload).text
            log("HTTP Response: {0}".format(http_response))
            json_response = json.loads(http_response)

        elif method == 'POST':

            log("URL: {0}".format(url_payload))

            http_response = requests.post(url_payload, data=data, files=files).text
            log("HTTP Response: {0}".format(http_response))
            json_response = json.loads(http_response)

    #except:
    #    pass

    return json_response

def _execute_test(url, token, data, method, files=None):

    log("----")
    log("TEST: {0}".format(url))
    #log("")

    success = False
    response = {}

    if True:
    #try:
        if token == None:
            url_payload = "{0}{1}?".format(ROOT_DOMAIN,url)
        else:
            if not 'admin' in url:

                log('Calling Client URL')

                # this is a client url, and needs a client)id
                # rather than a token
                url_payload = "{0}{1}?client_id={2}&".format(ROOT_DOMAIN,url,token)
            else:

                log('Calling Admin URL')

                url_payload = "{0}{1}?token={2}&".format(ROOT_DOMAIN,url,token)

        response = url_action(url_payload, data, method, files)

        if response['success'] == False:
            raise Exception('ERROR: Success = False')

        success = True

    #except:
    #    pass

    return success, response

def _validate(expected, response):

    valid = False

    try:
        for key in expected:
            if not key in response:
                raise Exception("missing key in response")
            if not isinstance(response[key], expected[key]['type']):
                raise Exception("Incorrect field type for '{0}'".format(key))
            if 'value' in expected[key]:
                if not  response[key] == expected[key]['value']:
                    raise Exception("invalid response value for '{0}'".format(key))
        valid = True
    except Exception, e:
        print "Validation Error: {0}".format(e)

    return valid

def run_tests():

    log("Launching tests ...")
    log("")

    log("Testing Assignments ...")

    success, payload = _execute_test(
        'admin/get_access_token.json',
        None,
        {
            'username': 'system',
            'password': hashlib.sha256('password').hexdigest(),
        },
        'GET',
    )
    valid = _validate(
        {
            "organization": {
                "type": basestring,
                "value": "Yellr",
            },
            "token": {
                "type": basestring,
            },
            "first_name": {
                "type": basestring,
                "value": "SYSTEM",
            },
            "last_name": {
                "type": basestring,
                "value": "USER",
            },
            "success": {
                "type": bool,
                "value": True,
            },
        },
        payload,
    )
    if not valid == True:
        raise Exception("admin/get_access_token.json did not validate")
    token = payload['token']

    success, payload = _execute_test(
        'admin/get_languages.json',
        token,
        {
            # no fields required
        },
        'GET',
    )
    valid = _validate(
        {
            "languages": {
                "type": list,
                "value": [
                    {"code": "en","name": "English"},
                    {"code": "es","name": "Spanish"},
                ],
            },
            "success": {
                "type": bool,
                "value": True,
            },
        },
        payload,
    )
    if not valid == True:
        raise Exception("admin/get_languages.json did not validate")
    languages = payload['languages']

    success, payload = _execute_test(
        'admin/get_question_types.json',
        token,
        {
            # no fields required
        },
        'GET',
    )
    valid = _validate(
        {
            "question_types": {
                "type": list,
                "values": [
                    {"question_type_text": "free_text", "question_type_id": 1, "question_type_description": "Free form text responce."},
                    {"question_type_text": "multiple_choice", "question_type_id": 2, "question_type_description": "Allows for up to ten multiple choice options"}
                ],
            },
            "success": {
                "type": bool,
                "value": True,
            },
        },
        payload,
    )
    if not valid == True:
        raise Exception("admin/get_question_types.json did not validate")
    question_types = payload['question_types']

    success, payload = _execute_test(
        'admin/create_question.json',
        token,
        {
            'language_code': 'en',
            'question_text': 'How will you be spending New Years Eve?',
            'description': 'Will you be doing anything special for New Years?!?',
            'question_type': 'free_text',
            #'answers': '',
        },
        'POST',
    )
    valid = _validate(
        {
            "question_text": {
                "type": basestring,
                "value": "How will you be spending New Years Eve?",
            },
            "description": {
                "type": basestring,
                "value": "Will you be doing anything special for New Years?!?",
            },
            "answers": {
                "type": list,
                "value": ["", "", "", "", "", "", "", "", "", ""],
            },
            "question_type": {
                "type": basestring,
                "value": "free_text",
            },
            "language_code": {
                "type": basestring,
                "value": "en",
            },
            "question_id": {
                "type": int,
            },
            "success": {
                "type": bool,
                "value": True,
            }
        },
        payload,
    )
    if not valid == True:
        raise Exception("admin/create_question.json did not validate")
    question_id = payload['question_id']

    success, payload = _execute_test(
        'admin/publish_assignment.json',
        token,
        {
            'name': 'New Years',
            'life_time': 24*7, # 1 week
            'questions': json.dumps([question_id]),
            'top_left_lat': 43.4,
            'top_left_lng': -77.9,
            'bottom_right_lat': 43.0,
            'bottom_right_lng': -77.3,
        },
        'POST',
    )
    """
    valid = _validate(
        {
            "life_time": {
                "type": int,
                "value": 168,
            },
            "questions": [3],
            "top_left_lng": -77.9,
            "top_left_lat": 43.4,
            "bottom_right_lat": 43.0,
            "bottom_right_lng": -77.3
            "success": true,
            "assignment_id": 1,
            "collection_id": 1,
            }
        },
        payload,
    )
    if not valid == True:
        raise Exception("admin/publish_assignment.json did not validate")
    """
    assignment_id = payload['assignment_id']
    collection_id = payload['collection_id']


    random_client_id = str(uuid.uuid4())
    success, payload = _execute_test(
        'get_assignments.json',
        random_client_id,
        {
            'language_code': 'en',
            'lat': 43.2,
            'lng': -77.5,
        },
        'GET',
    )
    assignments = payload['assignments']
    log('Assignment Count: {0}'.format(len(assignments)))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_my_collections.json',
        token,
        {
            # does not take any input fields
        },
        'GET',
    )
    collections = payload['collections']
    log('Collection Count: {0}'.format(len(collections)))
    if len(collections) != 1:
        raise Exception("Error: Created collection was not returned.")
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/create_collection.json',
        token,
        {
            'name': 'Random Things',
            'description': 'My collection of randomness',
            'tags': '',
        },
        'POST',
    )
    new_collection_id = payload['collection_id']
    log('New Collection ID: {0}'.format(new_collection_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_my_collections.json',
        token,
        {
            # does not take any input fields
        },
        'GET',
    )
    second_round_collections = payload['collections']
    log('Collection Count: {0}'.format(len(collections)))
    if len(second_round_collections) != 2:
        raise Exception("Error: Created collection was not returned.")
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_assignments.json',
        token,
        {
            # does not take any input fields
        },
        'POST',
    )
    assignments = payload['assignments']
    log('Assignment Count: {0}'.format(len(assignments)))
    if len(assignments) == 0:
        raise Exception("Error: Created assignment was not returned.")
    log('----')
    log('')
    log('')

    #
    # Create our Client ID """
    #
    client_id_a = str(uuid.uuid4())
    client_id_b = str(uuid.uuid4())
    client_id_c = str(uuid.uuid4())

    #
    # Create response post A
    #
    #

    success, payload = _execute_test(
        'upload_media.json',
        None,
        {
            'client_id': client_id_a,
            'media_type': 'text',
            'media_text': 'Hopefully staying awake long enough to see the ball drop ... :/',
        },
        'POST',
    )
    media_id_a = payload['media_id']
    log('Media Object ID: {0}'.format(media_id_a))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'publish_post.json',
        None,
        {
            'client_id': client_id_a,
            'assignment_id': assignment_id,
            'title': '',
            'language_code': 'en',
            'lat': 43.1,
            'lng': -77.5,
            'media_objects': json.dumps([media_id_a]),
        },
        'POST',
    )
    post_id_a = payload['post_id']
    log('Post ID: {0}'.format(post_id_a))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_user_posts.json',
        token,
        {
            'client_id': client_id_a,
        },
        'GET',
    )
    client_a_posts = payload['posts']
    log('Client Post Count: {0}'.format(len(client_a_posts)))
    if len(client_a_posts) != 1:
        raise Exception('Error: client_a post was not returned in list of user posts.')
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_post.json',
        token,
        {
            'post_id': client_a_posts[0]['post_id'],
        },
        'GET',
    )
    client_a_post_response = payload['post']
    if client_a_post_response['post_id'] != client_a_posts[0]['post_id']:
        raise Exception("incorrect post returned from get_post.json")
    log('Client A Post Response ID: {0}'.format(client_a_post_response['post_id']))
    log('----')
    log('')
    log('')

    #
    # Create response post B
    #

    success, payload = _execute_test(
        'upload_media.json',
        None,
        {
            'client_id': client_id_b,
            'media_type': 'text',
            'media_text': 'Going out to Da CLUB!!!',
        },
        'POST',
    )
    media_id_b = payload['media_id']
    log('Media Object ID: {0}'.format(media_id_b))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'publish_post.json',
        None,
        {
            'client_id': client_id_b,
            'assignment_id': assignment_id,
            'title': '',
            'language_code': 'en',
            'lat': 43.1,
            'lng': -77.5,
            'media_objects': json.dumps([media_id_b]),
        },
        'POST',
    )
    post_id_b = payload['post_id']
    log('Post ID: {0}'.format(post_id_b))
    log('----')
    log('')
    log('')


    #
    # Create response post C
    #

    success, payload = _execute_test(
        'upload_media.json',
        None,
        {
            'client_id': client_id_c,
            'media_type': 'text',
            'media_text': 'I like turtles.',
        },
        'POST',
    )
    media_id_c = payload['media_id']
    log('Media Object ID: {0}'.format(media_id_c))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'publish_post.json',
        None,
        {
            'client_id': client_id_c,
            'assignment_id': assignment_id,
            'title': '',
            'language_code': 'en',
            'lat': 43.1,
            'lng': -77.5,
            'media_objects': json.dumps([media_id_c]),
        },
        'POST',
    )
    post_id_c = payload['post_id']
    log('Post ID: {0}'.format(post_id_c))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_assignment_responses.json',
        token,
        {
            'assignment_id': assignment_id,
        },
        'GET',
    )
    response_posts = payload['posts']
    if len(response_posts) != 3:
        raise Exception('Corrent number of response posts were not seen')

    for i in range(0,len(response_posts)):
        log("Post {0}, post_id: {1} , media_id[0]: {2}".format(
            i,
            response_posts[i]['post_id'],
            response_posts[i]['media_objects'][0]['media_id'],
        ))

    # test contents (desc order)
    #if not (response_posts[0]['post_id'] == post_id_b and \
    #        response_posts[1]['post_id'] == post_id_a and \
    #        response_posts[0]['media_objects'][0]['media_id'] == media_id_b and \
    #        response_posts[1]['media_objects'][0]['media_id'] == media_id_a):
    #    raise Exception('Incorrect post id and/or media id')

    log('Response Count: {0}'.format(len(response_posts)))
    log('----')
    log('')
    log('')

    #
    # Delete post
    #

    success, payload = _execute_test(
        'admin/delete_post.json',
        token,
        {
            'post_id': post_id_c,
        },
        'POST',
    )
    deleted_post_id = payload['post_id']
    if not deleted_post_id == post_id_c:
        raise Exception("deleted post id did not match intended post")
    log('----')
    log('')
    log('')

    #
    # Get assignment responses to check that deleted post was actually deleted
    #
   
    success, payload = _execute_test(
        'admin/get_assignment_responses.json',
        token,
        {
            'assignment_id': assignment_id,
        },
        'GET',
    )
    response_posts = payload['posts']
    if len(response_posts) != 2:
        raise Exception('Corrent number of response posts were not seen')

    for i in range(0,len(response_posts)):
        log("Post {0}, post_id: {1} , media_id[0]: {2}".format(
            i,
            response_posts[i]['post_id'],
            response_posts[i]['media_objects'][0]['media_id'],
        ))

 

    success, payload = _execute_test(
        'admin/add_post_to_collection.json',
        token,
        {
            'collection_id': collection_id,
            'post_id': post_id_a,
        },
        'POST',
    )
    collection_post_id = payload['post_id']
    collection_collection_id = payload['collection_id']

    if not (collection_post_id == post_id_a and collection_collection_id == \
            collection_id):
        raise Exception('Post ID and Collection ID did not match after assignment.')

    log('Post ID: {0}'.format(collection_post_id))
    log('Collection ID: {0}'.format(collection_collection_id))
    log('----')
    log('')
    log('')

    post_collection_assignment_success = True
    try:
        success, payload = _execute_test(
            'admin/add_post_to_collection.json',
            token,
            {
                'collection_id': 99,
                'post_id': 100,
            },
            'POST',
        )
    except:
        post_collection_assignment_success = False

    if post_collection_assignment_success == True:
        raise Exception("Invalid collection and post were added.");
    log('Post-Collection assignment failed with invalid data.')
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_collection_posts.json',
        token,
        {
            'collection_id': collection_id,
        },
        'GET',
    )
    collection_posts = payload['posts']
    log('Collection Post Count: {0}'.format(len(collection_posts)))
    if len(collection_posts) != 1:
        raise Exception('Error: added post was not returned with collection posts.')
    log('----')
    log('')
    log('')


    #
    # Perform a free post with text
    #

    success, payload = _execute_test(
        'upload_media.json',
        None,
        {
            'client_id': client_id_a,
            'media_type': 'text',
            'media_text': 'I saw a policeman help walk an old lady accross the street today.',
        },
        'POST',
    )
    text_media_id = payload['media_id']
    log('Text Media Object ID: {0}'.format(text_media_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'publish_post.json',
        None,
        {
            'client_id': client_id_a,
            'assignment_id': '',
            'title': '',
            'language_code': 'en',
            'lat': 43.1,
            'lng': -77.5,
            'media_objects': json.dumps([text_media_id]),
        },
        'POST',
    )
    text_post_id = payload['post_id']
    log('Text Post ID: {0}'.format(text_post_id))
    log('----')
    log('')
    log('')

    #
    # Perform a free post with image
    #

    success, payload = _execute_test(
        'upload_media.json',
        None,
        {
            'client_id': client_id_a,
            'media_type': 'image',
        },
        'POST',
        files={'media_file': open('./test_media/roc.jpg','rb')},
    )
    image_media_id = payload['media_id']
    log('Image Media Object ID: {0}'.format(image_media_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'publish_post.json',
        None,
        {
            'client_id': client_id_a,
            'assignment_id': '',
            'title': '',
            'language_code': 'en',
            'lat': 43.1,
            'lng': -77.5,
            'media_objects': json.dumps([image_media_id]),
        },
        'POST',
    )
    image_1_post_id = payload['post_id']
    log('Image Post ID: {0}'.format(image_1_post_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/add_post_to_collection.json',
        token,
        {
            'collection_id': collection_id,
            'post_id': image_1_post_id,
        },
        'POST',
    )

    #
    # post another free post with image
    #

    success, payload = _execute_test(
        'upload_media.json',
        None,
        {
            'client_id': client_id_a,
            'media_type': 'image',
        },
        'POST',
        files={'media_file': open('./test_media/roc2.jpg','rb')},
    )
    image_media_id = payload['media_id']
    log('Image Media Object ID: {0}'.format(image_media_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'publish_post.json',
        None,
        {
            'client_id': client_id_a,
            'assignment_id': '',
            'title': '',
            'language_code': 'en',
            'lat': 43.1,
            'lng': -77.5,
            'media_objects': json.dumps([image_media_id]),
        },
        'POST',
    )
    image_2_post_id = payload['post_id']
    log('Image Post ID: {0}'.format(image_2_post_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/add_post_to_collection.json',
        token,
        {
            'collection_id': collection_id,
            'post_id': image_2_post_id,
        },
        'POST',
    )

    success, payload = _execute_test(
        'admin/get_collection_posts.json',
        token,
        {
            'collection_id': collection_id,
        },
        'GET',
    )
    collection_posts = payload['posts']
    log('Collection Post Count: {0}'.format(len(collection_posts)))
    if len(collection_posts) != 3:
        raise Exception('Error: added post was not returned with collection posts.')
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_my_collections.json',
        token,
        {
            # does not take any input fields
        },
        'GET',
    )
    collections = payload['collections']
    log('Collection Count: {0}'.format(len(collections)))
    if len(collections) != 2:
        raise Exception("Error: Created collection was not returned.")
    log('----')
    log('')
    log('')


    #
    # test if number of posts returned was correct
    #

    success, payload = _execute_test(
        'admin/get_posts.json',
        token,
        {
            # no fields required
        },
        'GET',
    )
    total_posts = payload['posts']
    if len(total_posts) < 5:
        raise Exception("Not all posts were returned.")
    log('Total Post Count: {0}'.format(len(total_posts)))
    log('----')
    log('')
    log('')






    #
    # Publish Story
    #

    success, payload = _execute_test(
        'admin/publish_story.json',
        token,
        {
            'title': "Bringing in 2015",
            'tags': 'new years, 2015',
            'top_text': 'Edited on December 24th, 2014 - 5:41pm',
            'banner_media_id': '-',
            'contents': "Looks like it's a split between partiers and shut-in's, folks.",
            'language_code': 'en',
            'top_left_lat': 45,
            'top_left_lng': -80,
            'bottom_right_lat': 42,
            'bottom_right_lng': -75,
        },
        'POST',
    )
    story_unique_id = payload['story_unique_id']
    log('Story Unique ID: {0}'.format(story_unique_id))
    log('----')
    log('')
    log('')

    new_user_client_id = str(uuid.uuid4())
    new_username = 'temp_user'
    new_password = hashlib.sha256('password123').hexdigest()

    success, payload = _execute_test(
        'admin/create_user.json',
        token,
        {
            'user_type_id': 2,
            'client_id': new_user_client_id,
            'username': new_username,
            'password': new_password,
            'first_name': 'Temp',
            'last_name': 'User',
            'email': 'temp@user.com',
            'organization': 'The Temp Group',
            'fence_top_left_lat': 43.4,
            'fence_top_left_lng': -77.9,
            'fence_bottom_right_lat': 43.0,
            'fence_bottom_right_lng': -77.3,
        },
        'POST',
    )
    new_user_id= payload['user_id']
    log('New User ID: {0}'.format(new_user_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_access_token.json',
        None,
        {
            'username': new_username,
            'password': new_password
        },
        'GET',
    )
    new_user_token = payload['token']
    log('Got New User Token: {0}'.format(new_user_token))
    log('----')
    log('')
    log('')


    log("Done with Tests")
    log("")

if __name__ == '__main__':

    print "\n\n"

    run_tests()
