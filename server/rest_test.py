import uuid
import requests
import json
import hashlib
import datetime
from datetime import timedelta
from time import sleep

base_url = "http://localhost:5003"

class Client(object):

    def __init__(self, cuid=str(uuid.uuid4()), lat=43.1, lng=-77.5, language_code='en', platform='test'):
        self.cuid = cuid
        self.lat = lat
        self.lng = lng
        self.language_code = language_code
        self.platform = platform

    def build_url(self, base_url):
        return base_url + '?cuid=' + self.cuid + '&lat=' + str(self.lat) + '&lng=' + str(self.lng) + '&language_code=' + self.language_code + '&platform=' + self.platform


class User(object):

    def __init__(self, username='system', password=hashlib.sha256('password'.encode('utf-8')).hexdigest(), token=''):
        self.username = username
        self.password = password
        self.token = ''
        self.cookies = None

    def build_url(self, base_url):
        return base_url

def get_client(client):
    url = base_url + '/api/clients'
    resp = requests.get(client.build_url(url))
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def get_posts(client):
    url = base_url + '/api/posts'
    resp = requests.get(client.build_url(url))
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def register_vote(client, post, is_up_vote):
    url = base_url + '/api/posts/{id}/vote'.replace('{id}', post['id'])
    data = json.dumps({
        'is_up_vote': is_up_vote,
    })
    resp = requests.post(client.build_url(url), data)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)


def publish_post(client, contents, assignment_id=None, poll_response=-1):
    url = base_url + '/api/posts'
    data = json.dumps({
        'contents': contents,
        'assignment_id': assignment_id,
        'poll_response': poll_response,
    })
    resp = requests.post(client.build_url(url), data)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def upload_media_object(client, post, media_type, filename):
    url = base_url + '/api/media_objects'
    data = {
        'media_type': media_type,
        'post_id': post['id'],
        'media_file': filename,
    }
    files = {'media_file': open(filename, 'rb')}
    resp = requests.post(client.build_url(url), data, files=files)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def get_assignments(client):
    url = base_url + '/api/assignments'
    resp = requests.get(client.build_url(url))
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def loggedin(user):
    url = base_url + '/api/admin/login'
    resp = requests.get(user.build_url(url), cookies=user.cookies)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def login(user):
    url = base_url + '/api/admin/login'
    data = json.dumps({
        'username': user.username,
        'password': user.password,
    })
    resp = requests.post(user.build_url(url), data)
    print('[' + str(resp.status_code) + ']')
    payload = json.loads(resp.text)
    user.token = payload['user']['token']
    user.cookies = resp.cookies
    return user

def logout(user):
    url = base_url + '/api/admin/logout'
    resp = requests.post(user.build_url(url), cookies=user.cookies)
    print('[' + str(resp.status_code) + ']')
    payload = json.loads(resp.text)
    #user.token = payload['user']['token']
    return user

def admin_get_posts(user):
    url = base_url + '/api/admin/posts'
    resp = requests.get(user.build_url(url), cookies=user.cookies)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def admin_update_post(user, post, deleted, flagged, approved):
    url = base_url + '/api/admin/posts/{id}'.replace('{id}', post['id'])
    data = json.dumps({
        'deleted': deleted,
        'flagged': flagged, 
        'approved': approved,
    })
    resp = requests.put(user.build_url(url), data, cookies=user.cookies)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def admin_create_assignment(user, name, life_time, top_left_lat, top_left_lng, bottom_right_lat, bottom_right_lng, question_type):
    url = base_url + '/api/admin/assignments'
    data = json.dumps({
        'life_time': str(life_time),
        'name': name,
        'top_left_lat': top_left_lat,
        'top_left_lng': top_left_lng,
        'bottom_right_lat': bottom_right_lat,
        'bottom_right_lng': bottom_right_lng,
        'question_type': question_type,
    })
    resp = requests.post(user.build_url(url), data, cookies=user.cookies)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def admin_create_question(user, assignment, langauge_code, question_text, description, answer0, answer1, answer2, answer3, answer4):
    url = base_url + '/api/admin/questions'
    data = json.dumps({
        'assignment_id': assignment['id'],
        'language_code': 'en',
        'question_text': question_text,
        'description': description,
        #'question_type': question_type,
        'answer0': answer0,
        'answer1': answer1,
        'answer2': answer2,
        'answer3': answer3,
        'answer4': answer4,
    })
    resp = requests.post(user.build_url(url), data, cookies=user.cookies)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

def admin_update_question(user, question, language_code, question_text, description, answer0, answer1, answer2, answer3, answer4):
    url = base_url + '/api/admin/questions/' + question['id']
    data = json.dumps({
        #'assignment_id': assignment['id'],
        'language_code': 'en',
        'question_text': question_text,
        'description': description,
        #'question_type': question_type,
        'answer0': answer0,
        'answer1': answer1,
        'answer2': answer2,
        'answer3': answer3,
        'answer4': answer4,
    })
    resp = requests.put(user.build_url(url), data, cookies=user.cookies)
    print('[' + str(resp.status_code) + ']')
    return json.loads(resp.text)

if __name__ == '__main__':

    client_a = Client(cuid='43c4e9c0-bb48-4cde-ad5a-00f24b43dbfc')
    client_b = Client(cuid='e8fda109-1452-404b-8024-d6d23d7d5f51')
    user_a = User()

    #
    # Test Get Client Information
    #

    print('[GET] /api/clients')
    client_resp_a = get_client(client_a)
    print('\tclient id: ' + client_resp_a['client']['id'])

    #
    # Text Text Post
    #

    print('[POST] /api/posts')
    text_post = publish_post(client_b, "Sometimes I just go outside and look at the clouds for hours ...");
    print('\tpost id: ' + text_post['post']['id'])

    #
    # Test Get Local Posts (with no response )
    # 

    print('[GET] /api/posts')
    posts = get_posts(client_a)
    print('\tpost count: ' + str(len(posts['posts'])))
    print(json.dumps(posts, indent=4))

    #
    # Test Image Post
    # 

    print('[POST] /api/posts')
    image_post = publish_post(client_a, "This is a test post!")
    print('\tpost id: ' + image_post['post']['id'])

    print('[POST] /api/media_objects')
    image_media_object = upload_media_object(client_a, image_post['post'], "image", "smiley.png")
    print('\tmedia object id: ' + image_media_object['media_object']['id']) 

    #
    # Test Video Post
    #

    print('[POST] /api/posts')
    video_post = publish_post(client_a, "The video is strong with this one ...")
    print('\tpost id: ' + video_post['post']['id'])

    print('[POST] /api/media_objects')
    video_media_object = upload_media_object(client_a, video_post['post'], "video", "video.mp4")
    print('\tmedia object id: ' + video_media_object['media_object']['id'])

    #
    # Test Audio Post
    #

    print('[POST] /api/posts')
    audio_post = publish_post(client_a, "My voice ... IT IS IN YOU!")
    print('\tpost id: ' + audio_post['post']['id'])

    print('[POST] /api/media_objects')
    audio_media_object = upload_media_object(client_a, audio_post['post'], "audio", "audio.mp3")
    print('\tmedia object id: ' + audio_media_object['media_object']['id'])

    #
    # Test moderator login
    #
 
    print("[GET] /api/admin/loggedin")
    logged_in_0 = loggedin(user_a)
    print("\tlogged in = " + str(logged_in_0['loggedin']))

    print("[POST] /api/admin/login")
    user_a = login(user_a)
    print('\ttoken: ' + str(user_a.token))
    
    print("[GET] /api/admin/loggedin")
    logged_in_0 = loggedin(user_a)
    print("\tlogged in = " + str(logged_in_0['loggedin']))
    if logged_in_0['loggedin'] == False:
        raise Exception('not logged in')

    print("[POST] /api/admin/logout")
    user_a = logout(user_a)
    print('\ttoken: ' + str(user_a.token))

    print("[GET] /api/admin/loggedin")
    logged_in_0 = loggedin(user_a)
    print("\tlogged in = " + str(logged_in_0['loggedin']))

    print("[POST] /api/admin/login")
    user_a = login(user_a)
    print('\ttoken: ' + str(user_a.token))

    #
    # Test approve post
    #

    print("[GET] /api/admin/posts")
    posts = admin_get_posts(user_a)
    print('\tpost count: ' + str(len(posts)) if posts != None else None)

    print("[PUT] /api/admin/posts/{id}")
    post = admin_update_post(user_a, image_post['post'], deleted=False, flagged=False, approved=True)
    print('\tpost id: ' + image_post['post']['id'])
    print('\tapproved: ' + str(post['post']['approved']))

    print("[PUT] /api/admin/posts/{id}")
    post = admin_update_post(user_a, video_post['post'], deleted=False, flagged=False, approved=True)
    print('\tpost id: ' + image_post['post']['id'])
    print('\tapproved: ' + str(post['post']['approved']))

    print("[GET] /api/posts")
    posts_a = get_posts(client_a)
    print('\tpost count:' + str(len(posts_a['posts'])))

    #
    # Test Voting
    #

    print('[POST] /api/post/{id}/vote')
    video_post_vote = register_vote(client_b, image_post['post'], True)
    print('vote id: ' + video_post_vote['vote']['id'])
    
    print('[GET] /api/posts')
    posts = get_posts(client_a)
    print('\tpost count: ' + str(len(posts['posts'])))
    print(json.dumps(posts, indent=4))

    #
    # Test Assignments
    #

    print("[POST] /api/admin/assignments")
    assignment_a = admin_create_assignment(user_a, "Test Assignment", 72, 43.4, -77.9, 43.0, -77.3, 'text')
    print("\tassignment id:" + assignment_a['assignment']['id'])

    print("[POST] /api/admin/question")
    question_a = admin_create_question(user_a, assignment_a['assignment'],'en', 'How is your day going?', 'Tell us about your day so far!', '', '', '', '', '')
    print('\tquestion id: ' + question_a['question']['id'])

    print('[GET] /api/assignments')
    assignments_a = get_assignments(client_a)
    print('\tassignment count' + str(len(assignments_a['assignments'])))
    #print(json.dumps(assignments_a, indent=4))

    #
    # Test Assignment response
    #

    print('[POST] /api/posts')
    response_post = publish_post(client_a, "My day is going great, thanks for asking!", assignment_id=assignment_a['assignment']['id'])
    print('\tassignment_id: ' + assignment_a['assignment']['id'] + ', post id: ' + response_post['post']['id'])

    print('[POST] /api/media_objects')
    response_media_object = upload_media_object(client_a, response_post['post'], "image", "smiley.png")
    print('\tmedia object id: ' + response_media_object['media_object']['id'])

    print("[PUT] /api/admin/posts/{id}")
    post = admin_update_post(user_a, response_post['post'], deleted=False, flagged=False, approved=True)
    print('\tapproved: ' + str(post['post']['approved']))

    #
    # Test Update Assignment Question
    # 

    print("[POST] /api/admin/assignments")
    assignment_b = admin_create_assignment(user_a, "Tell me about the wind ...", 72, 43.4, -77.9, 43.0, -77.3, 'text')
    print("\tassignment id:" + assignment_a['assignment']['id'])

    print("[POST] /api/admin/question")
    question_b = admin_create_question(user_a, assignment_b['assignment'],'en', 'Tell me about the wind ...', 'OMG TELL ME.', '', '', '', '', '')
    print('\tquestion id: ' + question_b['question']['id'])

    print('[GET] /api/assignments')
    assignments_b = get_assignments(client_a)
    print('\tassignment count: ' + str(len(assignments_b['assignments'])))
    #print(json.dumps(assignments_b, indent=4))

    print("[PUT] /api/admin/question")
    question_c = admin_update_question(user_a, question_b['question'], 'en', 'Tell me about the wind ... maybe?', 'OMG TELL ME ... if you want :/', '', '', '', '', '')
    print('\tquestion id: ' + question_c['question']['id'])

    print('[GET] /api/assignments')
    assignments_c = get_assignments(client_a)
    #print(json.dumps(assignments_c, indent=4))
    print('\tassignment count' + str(len(assignments_c['assignments'])))

    #
    # Test Delete Post
    #

    print('[POST] /api/posts')
    deleted_post = publish_post(client_b, "I poop on you!");
    print('\tpost id: ' + deleted_post['post']['id'])

    print("[PUT] /api/admin/posts/{id}")
    post = admin_update_post(user_a, deleted_post['post'], deleted=True, flagged=False, approved=False)
    print('\tapproved: ' + str(post['post']['approved']))

    print("[GET] /api/admin/posts")
    posts = admin_get_posts(user_a)
    #print(json.dumps(posts, indent=4))
    print('\tpost count: ' + str(len(posts['posts'])))

    #
    # Test Polls
    #

    print("[POST] /api/admin/assignments")
    poll_assignment = admin_create_assignment(user_a, "Test Poll Assignment", 72, 43.4, -77.9, 43.0, -77.3, 'poll')
    print("\tassignment id:" + poll_assignment['assignment']['id'])

    print("[POST] /api/admin/question")
    poll_question = admin_create_question(
        user_a,
        poll_assignment['assignment'],
        'en',
        'What is your favorite Color?',
        "You've got to have a favorite color, tell us which one it is!",
        'Red',
        'Green',
        'Blue',
        'Black',
        'Other',
    )
    print('\tquestion id: ' + question_a['question']['id'])

    print('[GET] /api/assignments')
    poll_assignments = get_assignments(client_a)
    print('\tassignment count' + str(len(poll_assignments['assignments'])))

    print('[POST] /api/posts')
    poll_response_post = publish_post(client_a, "", assignment_id=poll_assignment['assignment']['id'], poll_response=1) # green
    print('\tassignment_id: ' + poll_assignment['assignment']['id'] + ', post id: ' + poll_response_post['post']['id'])

    print("[PUT] /api/admin/posts/{id}")
    poll_post = admin_update_post(user_a, poll_response_post['post'], deleted=False, flagged=False, approved=True)
    print('\tapproved: ' + str(poll_post['post']['approved']))

    print('[GET] /api/posts')
    posts = get_posts(client_a)
    print('\tpost count: ' + str(len(posts['posts'])))
 
    print('[GET] /api/assignments')
    poll_assignments = get_assignments(client_a)
    print('\tassignment count' + str(len(poll_assignments['assignments'])))
