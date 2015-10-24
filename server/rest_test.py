import uuid
import requests
import json
import hashlib
import datetime
from datetime import timedelta


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
    return json.loads(resp.text)

def get_posts(client):
    url = base_url + '/api/posts'
    resp = requests.get(client.build_url(url))
    return json.loads(resp.text)

def publish_post(client, contents, assignment_id=None):
    url = base_url + '/api/posts'
    data = json.dumps({
        'assignment_id': assignment_id,
        'contents': contents,
    })
    resp = requests.post(client.build_url(url), data)
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
    return json.loads(resp.text)

def get_assignments(client):
    url = base_url + '/api/assignments'
    resp = requests.get(client.build_url(url))
    return json.loads(resp.text)

def loggedin(user):
    url = base_url + '/api/admin/login'
    resp = requests.get(user.build_url(url), cookies=user.cookies)
    return json.loads(resp.text)

def login(user):
    url = base_url + '/api/admin/login'
    data = json.dumps({
        'username': user.username,
        'password': user.password,
    })
    resp = requests.post(user.build_url(url), data)
    payload = json.loads(resp.text)
    #print(json.dumps(payload, indent=4))
    user.token = payload['user']['token']
    user.cookies = resp.cookies
    return user

def logout(user):
    url = base_url + '/api/admin/logout'
    resp = requests.post(user.build_url(url), cookies=user.cookies)
    payload = json.loads(resp.text)
    user.token = payload['user']['token']
    return user

def admin_get_posts(user):
    url = base_url + '/api/admin/posts'
    resp = requests.get(user.build_url(url), cookies=user.cookies)
    return json.loads(resp.text)

def admin_update_post(user, post, deleted, flagged, approved):
    url = base_url + '/api/admin/posts/{id}'.replace('{id}', post['id'])
    data = json.dumps({
        'deleted': deleted,
        'flagged': flagged, 
        'approved': approved,
    })
    resp = requests.put(user.build_url(url), data, cookies=user.cookies)
    return json.loads(resp.text)

def admin_create_assignment(user, name, life_time, top_left_lat, top_left_lng, bottom_right_lat, bottom_right_lng):
    url = base_url + '/api/admin/assignments'
    data = json.dumps({
        'life_time': str(life_time),
        'name': name,
        'top_left_lat': top_left_lat,
        'top_left_lng': top_left_lng,
        'bottom_right_lat': bottom_right_lat,
        'bottom_right_lng': bottom_right_lng,
    })
    resp = requests.post(user.build_url(url), data, cookies=user.cookies)
    return json.loads(resp.text)

def admin_create_question(user, assignment, langauge_code, question_text, description, question_type, answer0, answer1, answer2, answer3, answer4):
    url = base_url + '/api/admin/questions'
    data = json.dumps({
        'assignment_id': assignment['id'],
        'language_code': 'en',
        'question_text': question_text,
        'description': description,
        'question_type': question_type,
        'answer0': answer0,
        'answer1': answer1,
        'answer2': answer2,
        'answer3': answer3,
        'answer4': answer4,
    })
    resp = requests.post(user.build_url(url), data, cookies=user.cookies)
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
    print(resp.text)
    return json.loads(resp.text)

if __name__ == '__main__':

    client_a = Client(cuid='43c4e9c0-bb48-4cde-ad5a-00f24b43dbfc')
    user_a = User()

    print('[GET] /api/clients')
    client_resp_a = get_client(client_a)
    print('client id: ' + client_resp_a['client']['id'])

    print('[GET] /api/posts')
    posts_a = get_posts(client_a)
    print('\tpost count: ' + str(len(posts_a['posts'])))

    print('[POST] /api/posts')
    post_0_a = publish_post(client_a, "This is a test post!")
    print('\tpost id: ' + post_0_a['post']['id'])

    print('[POST] /api/media_objects')
    media_object_0_a = upload_media_object(client_a, post_0_a['post'], "image", "smiley.png")
    #print(json.dumps(media_object_0_a, indent=4))
    print('\tmedia object id: ' + media_object_0_a['media_object']['id'])

    print("[GET] /api/admin/loggedin")
    logged_in_0 = loggedin(user_a)
    print("\tlogged in = " + str(logged_in_0['loggedin']))

    print("[POST] /api/admin/login")
    user_a = login(user_a)
    print('\ttoken: ' + str(user_a.token))

    print("[GET] /api/admin/loggedin")
    logged_in_0 = loggedin(user_a)
    print("\tlogged in = " + str(logged_in_0['loggedin']))

    print("[POST] /api/admin/logout")
    user_a = logout(user_a)
    print('\ttoken: ' + str(user_a.token))

    print("[GET] /api/admin/loggedin")
    logged_in_0 = loggedin(user_a)
    print("\tlogged in = " + str(logged_in_0['loggedin']))

    print("[POST] /api/admin/login")
    user_a = login(user_a)
    print('\ttoken: ' + str(user_a.token))

    print("[GET] /api/admin/posts")
    posts = admin_get_posts(user_a)
    print('\tpost count: ' + str(len(posts)) if posts != None else None)

    print("[PUT] /api/admin/posts/{id}")
    post = admin_update_post(user_a, post_0_a['post'], deleted=False, flagged=False, approved=True)
    print('\tapproved: ' + str(post['post']['approved']))

    print("[GET] /api/posts")
    posts_a = get_posts(client_a)
    print('\tpost count:' + str(len(posts_a['posts'])))
    print(json.dumps(posts_a, indent=4))

    print("[POST] /api/admin/assignments")
    assignment_a = admin_create_assignment(user_a, "Test Assignment", 72, 43.4, -77.9, 43.0, -77.3)
    print("\tassignment id:" + assignment_a['assignment']['id'])

    print("[POST] /api/admin/question")
    question_a = admin_create_question(user_a, assignment_a['assignment'],'en', 'How is your day going?', 'Tell us about your day so far!', 'text', '', '', '', '', '')
    print('\tquestion id: ' + question_a['question']['id'])

    print('[GET] /api/assignments')
    assignments_a = get_assignments(client_a)
    print(json.dumps(assignments_a, indent=4))

    print('[POST] /api/posts')
    post_1_a = publish_post(client_a, "My day is going great, thanks for asking!", assignment_id=assignment_a['assignment']['id'])
    print('\tassignment_id: ' + assignment_a['assignment']['id'] + ', post id: ' + post_1_a['post']['id'])

    print('[POST] /api/media_objects')
    media_object_1_a = upload_media_object(client_a, post_1_a['post'], "image", "smiley.png")
    #print(json.dumps(media_object_0_a, indent=4))
    print('\tmedia object id: ' + media_object_0_a['media_object']['id'])

    print("[PUT] /api/admin/posts/{id}")
    post = admin_update_post(user_a, post_1_a['post'], deleted=False, flagged=False, approved=True)
    print('\tapproved: ' + str(post['post']['approved']))

    print("[POST] /api/admin/assignments")
    assignment_b = admin_create_assignment(user_a, "Tell me about the wind ...", 72, 43.4, -77.9, 43.0, -77.3)
    print("\tassignment id:" + assignment_a['assignment']['id'])

    print("[POST] /api/admin/question")
    question_b = admin_create_question(user_a, assignment_b['assignment'],'en', 'Tell me about the wind ...', 'OMG TELL ME.', 'text', '', '', '', '', '')
    print('\tquestion id: ' + question_b['question']['id'])

    print('[GET] /api/assignments')
    assignments_b = get_assignments(client_a)
    print(json.dumps(assignments_b, indent=4))

    print("[PUT] /api/admin/question")
    question_c = admin_update_question(user_a, question_b['question'], 'en', 'Tell me about the wind ... maybe?', 'OMG TELL ME ... if you want :/', '', '', '', '', '')
    print('\tquestion id: ' + question_c['question']['id'])

    print('[GET] /api/assignments')
    assignments_c = get_assignments(client_a)
    print(json.dumps(assignments_c, indent=4))
