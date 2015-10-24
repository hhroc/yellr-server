from pyramid.response import Response
from pyramid.view import view_defaults
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    #DBSession,
    #MyModel,
    Users,
    Assignments,
    Questions,
    Collections,
    Posts,
    MediaObjects,
    Clients,
    )

import datetime
from datetime import timedelta

def get_payload(request):
    try:
        payload = request.json_body
    except:
        payload = None
    return payload

def build_paging(request):
    start = 0
    count = 50
    if 'start' in request.GET and 'count' in request.GET:
        try:
            start = int(float(request.GET['start']))
            count = int(float(request.GET['count']))
            if count > 50:
                count = 50
        except:
            start = 0
            count = 50
    return start, count


def authenticate(request):
    user = None
    token = False
    try:
        token = request.session['token']
    except:
        pass
    if token:
        user = Users.get_from_token(token)
    return user
    

@view_defaults(route_name='/api/admin/login', renderer='json')
class AdminLoginAPI(object):

    post_req = (
        'username',
        'password',
    )

    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='POST')
    def post(self):
        resp = {'user': None}
        payload = get_payload(self.request)
        if payload and all(r in payload for r in self.post_req):
            user = Users.authenticate(
                username=payload['username'],
                password=payload['password'],
            )
            resp = {'user': user.to_dict()}
            self.request.session['token'] = user.token
        else:
            self.request.response.status = 403
        return resp


@view_defaults(route_name='/api/admin/logout', renderer='json')
class AdminLogoutAPI(object):

    def __init__(self, request):
        self.request = request

    @view_config(request_method='POST')
    def post(self):
        resp = {'user': None}
        token = self.request.session['token']
        if token:
            user = Users.invalidate_token(token)
            resp = {'user': user.to_dict()}
        return resp    


@view_defaults(route_name='/api/admin/posts', renderer='json')
class AdminPostsAPI(object):

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='GET')
    def get(self):
        resp = {'posts': None}
        if self.user:
            _posts = Posts.get_posts(
                top_left_lat=self.user.geo_fence.top_left_lat,
                top_left_lng=self.user.geo_fence.top_left_lng,
                bottom_right_lat=self.user.geo_fence.bottom_right_lat,
                bottom_right_lng=self.user.geo_fence.bottom_right_lng,
            )
            posts = [p.to_dict(None) for p in _posts]
            resp = {'posts': posts}
        else:
            self.request.response.status = 403
        return resp

@view_defaults(route_name='/api/admin/posts/{id}', renderer='json')
class AdminPostAPI(object):

    put_req = (
        'deleted',
        'flagged',
        'approved',
    )

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='PUT')
    def put(self):
        resp = {'post': None}
        payload = get_payload(self.request)
        if self.user and payload and all(r in payload for r in self.put_req):
            post = Posts.get_by_id(self.request.matchdict['id'])
            post = Posts.update_by_id(
                post.id,
                client_id = post.client_id,
                assignment_id = post.assignment_id,
                language_code = post.language_code,
                lat = post.lat,
                lng = post.lng,
                contents = post.contents,
                deleted = bool(payload['deleted']),
                flagged = bool(payload['flagged']),
                approved = bool(payload['approved']),
            )
            resp = {'post': post.to_dict(None)}
        else:
            self.request.response.status = 403
        return resp


@view_defaults(route_name='/api/admin/assignments', renderer='json')
class AdminAssignmentsAPI(object):

    post_req = (
        'life_time',
        'name',
        'top_left_lat',
        'top_left_lng',
        'bottom_right_lat',
        'bottom_right_lng',
    )

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='GET')
    def get(self):
        resp = {'assignments': None}
        if self.user:
            _assignments = Assignments.get_all()
            assignments = [a.to_dict() for a in _assignments]
            resp = {'assignments': assignments}
        else:
            self.request.response.status = 403
        return resp

    @view_config(request_method='POST')
    def post(self):
        resp = {'assignment': None}
        payload = get_payload(self.request)
        if self.user and payload and all(r in payload for r in self.post_req): 
            collection = Collections.add(
                user_id=self.user.id,
                name=payload['name'],
                description='Collection for Assignment: ' + payload['name'],
                tags='',
                enabled=True,
            )
            assignment = Assignments.add(
                user_id=self.user.id,
                expire_datetime=datetime.datetime.now() + timedelta(hours=float(payload['life_time'])),
                name=payload['name'],
                top_left_lat=payload['top_left_lat'],
                top_left_lng=payload['top_left_lng'],
                bottom_right_lat=payload['bottom_right_lat'],
                bottom_right_lng=payload['bottom_right_lng'],
                collection_id=collection.id,
            )
            resp = {'assignment': assignment.to_dict()}
        else:
            self.response.request.status = 400
        return resp

@view_defaults(route_name='/api/admin/questions', renderer='json')
class AdminQuestionsAPI(object):

    post_req = (
        'assignment_id',
        'language_code',
        'question_text',
        'description',
        'question_type',
        'answer0',
        'answer1',
        'answer2',
        'answer3',
        'answer4',
    )

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='POST')
    def post(self):
        resp = {'question': None}
        payload = get_payload(self.request)
        print(payload)
        print(all(r in payload for r in self.post_req))
        if self.user and payload and all(r in payload for r in self.post_req):
            print('inside')
            question = Questions.add(
                user_id=self.user.id,
                assignment_id=payload['assignment_id'],
                language_code=payload['language_code'],
                question_text=payload['question_text'],
                description=payload['description'],
                question_type=payload['question_type'],
                answer0=payload['answer0'],
                answer1=payload['answer1'],
                answer2=payload['answer2'],
                answer3=payload['answer3'],
                answer4=payload['answer4'],
            )
            resp = {'question': question.to_dict()}
        else:
            self.request.response.status = 400
        return resp

@view_defaults(route_name='/api/admin/collections', renderer='json')
class AdminCollectionsAPI(object):

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='GET')
    def get(self):
        resp = {'collections': None}
        
        return resp

"""
@view_defaults(route_name='/api/assignments', renderer='json')
class AssignmentsAPI(object):

    def __init__(self, request):
        self.request = request
        start, count = build_paging(request)
        self.client = check_in(request)

    # [ GET ] - get local assignments
    @view_config(request_method='GET')
    def get(self):
        resp = {'assignments': []}
        if self.client:
            start, count = build_paging(self.request)
            resp = Assignments.get_all_open(client.last_lat, client.last_lng)
        else:
            self.request.response.status = 403
        return resp


@view_defaults(route_name='/api/posts', renderer='json')
class PostsAPI(object):

    post_req = (
        'assignment_id',
        'contents',
    )

    def __init__(self, request):
        self.request = request
        self.start, self.count = build_paging(request)
        self.client = check_in(request)

    # [ GET ] - get local posts
    @view_config(request_method='GET')
    def get(self):
        resp = {'posts': []}
        if self.client:
            start, count = build_paging(self.request)
            _posts = Posts.get_approved_posts(
                lat=self.client.last_lat,
                lng=self.client.last_lng,
                start=self.start,
                count=self.count,
            )
            posts = [p.to_dict(self.client.id) for p in _posts]
            resp = {'posts': posts}
        else:
            self.request.response.status = 403
        return resp

    # [ POST ] - create new post
    @view_config(request_method='POST')
    def post(self):
        resp = {'post': None}
        payload = get_payload(self.request)
        if payload and all(r in payload for r in self.post_req) and self.client:
            try:
                assignment_id = int(float(payload['assignment_id']))
            except:
                assignment_id = None
            print(self.client.id)
            print(self.client.cuid)
            post = Posts.add(
                client_id=self.client.id,
                assignment_id=assignment_id,
                lat=self.client.last_lat,
                lng=self.client.last_lng,
                language_code=self.client.language_code,
                contents=payload['contents'],
                deleted=False,
                approved=False,
                flagged=False,
            )
            resp = {'post': post.to_dict(self.client.id)}
        else:
            self.request.response.status = 403
        return resp


@view_defaults(route_name='/api/posts/{id}/media_objects', renderer='json')
class MediaObjectsAPI(object):

    post_req = (
        '',
    )

    def __init__(self, request):
        self.request = request

    # [ POST ] - creates media object against a post
    @view_config(request_method='POST')
    def post(self):
        resp = {'media_object': None}
        return resp


@view_defaults(route_name='/api/posts/{id}/vote', renderer='json')
class VoteAPI(object):

    post_req = (
        'post_id',
        'is_up_vote',
    )

    def __init__(self, request):
        self.request = request

    # [ POST ] - votes on a post
    @view_config(request_method='POST')
    def post(self):
        resp = {'vote': None}
        if payload and all(r in payload for r in self.post_req) and self.client:
            vote = Votes.register_vote(
                post_id=payload['post_id'],
                client_id=self.client.id,
                is_up_vote=payload['is_up_vote']
            )
        else:
            self.request.response.status = 403
        return resp


@view_defaults(route_name='/api/posts/{id}/flag')
class FlagAPI(object):

    post_req = (
        'post_id',
    )

    def __init__(self, request):
        self.request = request
        self.client = check_in(request)

    # [ POST ] - flags a post
    @view_config(request_method='POST')
    def post(self):
        resp = {'post': None}
        if payload and all(r in payload for r in self.post_req) and self.client:
            post = Posts.flag_post(
                post_id=payload['post_id'],
            )
            resp = {'post': post.to_dict()}
        else:
            self.request.response.status = 403
        return resp


@view_defaults(route_name='/api/clients')
class ClientsAPI(object):

    def __init__(self, request):
        self.request = request
    
    # [ GET ] - get clients profile
    @view_config(request_method='GET')
    def get(self):
        resp = {}
        return resp

    # [ PUT ] - updates a clients profile
    @view_config(request_method='PUT')
    def put(self):
        resp = {}
        return resp

    # [ DELETE ] - marks the client as deleted ( forgotten )
    @view_config(request_method='DELETE')
    def delete(self):
        resp = {}
        
        return resp
"""
