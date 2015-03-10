from tests import _execute_test, log

import uuid
import hashlib
import json

if __name__ == '__main__':

    _language_code = 'en'
    _lat = 43.2
    _lng = -77.5

    random_client_id = str(uuid.uuid4())
    success, payload = _execute_test(
        'get_assignments.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {},
        'GET',
    )
    assignments = payload['assignments']
    log('Assignment Count: {0}'.format(len(assignments)))
    log('----')

    success, payload = _execute_test(
        'get_stories.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {},
        'GET',
    )
    stories = payload['stories']
    log('Story Count: {0}'.format(len(stories)))
    log('----')
 
    success, payload = _execute_test(
        'get_notifications.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {},
        'GET',
    )
    notifications = payload['notifications']
    log('Notification Count: {0}'.format(len(notifications)))
    log('----')

    success, payload = _execute_test(
        'get_messages.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {},
        'GET',
    )
    messages = payload['messages']
    log('Messages Count: {0}'.format(len(messages)))
    log('----')

    success, payload = _execute_test(
        'get_profile.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {},
        'GET',
    )
    log('----')

    success, payload = _execute_test(
        'upload_media.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {
            #'client_id': random_client_id,
            'media_type': 'text',
            'media_text': 'Four score and seven years ago, our fathers brought ...',
        },
        'POST',
    )
    media_id_text = payload['media_id']
    log('Media Object ID (Text): {0}'.format(media_id_text))
    log('----')

    success, payload = _execute_test(
        'publish_post.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {
            #'client_id': client_id_a,
            'assignment_id': 0, #assignment_id,
            #'title': '',
            #'language_code': 'en',
            #'lat': 43.1,
            #'lng': -77.5,
            'media_objects': json.dumps([media_id_text]),
        },
        'POST',
    )
    post_id_text = payload['post_id']
    log('Post ID (Text): {0}'.format(post_id_text))
    log('----')
    
    success, payload = _execute_test(
        'upload_media.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {
            #'client_id': client_id,
            'media_type': 'image',
        },
        'POST',
        files={'media_file': open('./test_media/roc.jpg','rb')},
    )
    media_id_image = payload['media_id']
    log('Image Media Object ID (Image): {0}'.format(media_id_image))
    log('----')

    success, payload = _execute_test(
        'publish_post.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {
            #'client_id': client_id_a,
            'assignment_id': 0, #assignment_id,
            #'title': '',
            #'language_code': 'en',
            #'lat': 43.1,
            #'lng': -77.5,
            'media_objects': json.dumps([media_id_image]),
        },
        'POST',
    )
    post_id_image = payload['post_id']
    log('Post ID (Text): {0}'.format(post_id_image))
    log('----')

    success, payload = _execute_test(
        'get_approved_posts.json',
        random_client_id,
        _language_code,
        _lat,
        _lng,
        {},
        'GET',
    )
    approved_posts = payload['posts']
    log('Approved Posts: {0}'.format(approved_posts))
    log('----')

