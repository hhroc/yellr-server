import uuid
import requests
import json
import hashlib

base_url = "http://localhost:5003"

class Client(object):

    def __init__(self, cuid=str(uuid.uuid4()), lat=43.5, lng=-77.1, language_code='en', platform='test'):
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

def get_posts(client):
    url = base_url + '/api/posts'
    resp = requests.get(client.build_url(url))
    return json.loads(resp.text)

def publish_post(client, contents):
    url = base_url + '/api/posts'
    data = json.dumps({
        'assignment_id': '',
        'contents': contents,
    })
    resp = requests.post(client.build_url(url), data)
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

if __name__ == '__main__':

    client_a = Client(cuid='43c4e9c0-bb48-4cde-ad5a-00f24b43dbfc')
    user_a = User()

    print('[GET] /api/posts')
    posts_a = get_posts(client_a)
    print('\tpost count: ' + str(len(posts_a['posts'])))

    print('[POST] /api/posts')
    post_0_a = publish_post(client_a, "This is a test post!")
    print('\tpost id: ' + post_0_a['post']['id'])

    print('[POST] /api/media_objects')
    media_object_0_a = upload_media_object(client_a, "image", "smile.jpg")
    print('\tmedia object id: ' + media_object_0_a['media_object']['id']

    print("[POST] /api/admin/login")
    user_a = login(user_a)
    print('\ttoken: ' + str(user_a.token))

    print("[POST] /api/admin/logout")
    user_a = logout(user_a)
    print('\ttoken: ' + str(user_a.token))

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

    print("[POST] /api/
