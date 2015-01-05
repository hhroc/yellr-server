
import uuid
import json
import requests
import datetime
import hashlib

ROOT_DOMAIN = "http://127.0.0.1:5002/"

def log(output):

    print "[{0}]: {1}".format(str(datetime.datetime.now()).split('.')[0],output)

def url_action(url_payload, data, method):

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
            json_response = json.loads(http_response)

        elif method == 'POST':

            log("URL: {0}".format(url_payload))

            http_response = requests.post(url_payload, data=data).text
            json_response = json.loads(http_response)

        #log("HTTP Response: {0}".format(json_response))

    #except:
    #    pass

    return json_response

def _execute_test(url, token, data, method):

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

        response = url_action(url_payload, data, method)

        if response['success'] == False:
            raise Exception('ERROR: Success = False')

        success = True

    #except:
    #    pass

    return success, response


def run_tests():

    log("Launching tests ...")
    log("")

    success, payload = _execute_test(
        'admin/get_access_token.json',
        None,
        {
            'username': 'system',
            'password': hashlib.sha256('password').hexdigest(),
        },
        'GET',
    )
    token = payload['token']
    log('Got Token: {0}'.format(token))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_languages.json',
        token,
        {
            # no fields required
        },
        'GET',
    )
    languages = payload['languages']
    if len(languages) < 1:
        raise Exception('Invalid number of languages returned.')
    for language in languages:
        log('language: {0}, code: {1}'.format(language['name'], language['code']))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_question_types.json',
        token,
        {
            # no fields required
        },
        'GET',
    )
    question_types = payload['question_types']
    if len(languages) < 1:
        raise Exception('Invalid number of question_types returned.')
    for question_type in question_types:
        log("question_type: '{0}', id: {1}".format(
            question_type['question_type_text'], question_type['question_type_id']
        ))
    log('----')
    log('')
    log('')

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
    question_id = payload['question_id']
    log('Question ID: {0}'.format(question_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/publish_assignment.json',
        token,
        {
            'life_time': 24*7, # 1 week
            'questions': json.dumps([question_id]),
            'top_left_lat': 43.4,
            'top_left_lng': -77.9,
            'bottom_right_lat': 43.0,
            'bottom_right_lng': -77.3,
        },
        'POST',
    )
    assignment_id = payload['assignment_id']
    log('Assignment ID: {0}'.format(assignment_id))
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

    success, payload = _execute_test(
        'admin/get_assignment_responses.json',
        token,
        {
            'assignment_id': assignment_id,
        },
        'GET',
    )
    response_posts = payload['posts']
    if len(response_posts) < 2:
        raise Exception('Corrent number of response posts were not seen')

    for i in range(0,len(response_posts)):
        log("Post {0}, post_id: {1} , media_id[0]: {2}".format(
            i,
            response_posts[i]['post_id'],
            response_posts[i]['media_objects'][0]['media_id'],
        ))

    # test contents (desc order)
    if not (response_posts[0]['post_id'] == post_id_b and \
            response_posts[1]['post_id'] == post_id_a and \
            response_posts[0]['media_objects'][0]['media_id'] == media_id_b and \
            response_posts[1]['media_objects'][0]['media_id'] == media_id_a):
        raise Exception('Incorrect post id and/or media id')

    log('Response Count: {0}'.format(len(response_posts)))
    log('----')
    log('')
    log('')

    #
    # Perform a free post
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
    media_id = payload['media_id']
    log('Media Object ID: {0}'.format(media_id))
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
            'media_objects': json.dumps([media_id]),
        },
        'POST',
    )
    post_id = payload['post_id']
    log('Post ID: {0}'.format(post_id))
    log('----')
    log('')
    log('')

    success, payload = _execute_test(
        'admin/get_posts.json',
        token,
        {
            # no fields required
        },
        'GET',
    )
    total_posts = payload['posts']
    if len(total_posts) < 3:
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
