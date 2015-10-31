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
    #Collections,
    Posts,
    MediaObjects,
    Clients,
    )

import datetime
from datetime import timedelta
import json

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
    token = None
    user = None
    try:
        token = request.session['token']
    except:
        pass
    if token:
        user = Users.get_by_token(token)
    return user
    

@view_defaults(route_name='/login')
class AdminLoginScreen(object):

    def __init__(self, request):
        print('/login')
        self.request = request

    @view_config(request_method='GET', renderer='templates/login.pt')
    def get(self):
        return {} 


@view_defaults(route_name='/api/admin/login', renderer='json')
class AdminLoginAPI(object):

    post_req = (
        'username',
        'password',
    )

    def __init__(self, request):
        print('/api/admin/login')
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='GET')
    def get(self):
        resp = {'loggedin': False}
        if self.user:
            resp = {'loggedin': True}
        return resp
        
    @view_config(request_method='POST')
    def post(self):
        self.user = None
        self.request.session['token'] = None
        resp = {'user': None}
        payload = get_payload(self.request)
        if payload and all(r in payload for r in self.post_req):
            user = Users.authenticate(
                username=payload['username'],
                password=payload['password'],
            )
            if user:
                resp = {'user': user.to_dict()}
                self.request.session['token'] = user.token
            else:
                self.request.response.status = 403
        else:
            self.request.response.status = 400
        return resp


@view_defaults(route_name='/api/admin/logout', renderer='json')
class AdminLogoutAPI(object):

    def __init__(self, request):
        print('/api/admin/logout')
        self.request = request
        self.user = authenticate(request)

    @view_config()
    def post(self):
        resp = {'user': None}
        token = self.request.session['token']
        if token:
            user = Users.invalidate_token(token)
            if not user:
                self.request.response.stats = 403
        return resp    


@view_defaults(route_name='/api/admin/posts', renderer='json')
class AdminPostsAPI(object):

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='GET')
    def get(self):
        resp = {'posts': None}
        deleted = False
        if 'deleted' in self.request.GET:
            deleted = bool(self.request.GET['deleted'])
        if self.user:
            _posts = Posts.get_posts(
                top_left_lat=self.user.user_geo_fence.top_left_lat,
                top_left_lng=self.user.user_geo_fence.top_left_lng,
                bottom_right_lat=self.user.user_geo_fence.bottom_right_lat,
                bottom_right_lng=self.user.user_geo_fence.bottom_right_lng,
                deleted=deleted,
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
        print('/api/admin/posts')
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

    @view_config(request_method='GET')
    def get(self):
        resp = {'post': None}
        if self.user:
            id = self.request.matchdict['id']
            post = Posts.get_post_by_id(id)
            if post:
                resp = {'post': post.to_dict(None)}
            else:
                self.request.response.status = 404
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
        'question_type',
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
        if self.user:
            if payload and all(r in payload for r in self.post_req): 
                assignment = Assignments.add(
                    user_id=self.user.id,
                    expire_datetime=datetime.datetime.now() + timedelta(hours=float(payload['life_time'])),
                    name=payload['name'],
                    top_left_lat=payload['top_left_lat'],
                    top_left_lng=payload['top_left_lng'],
                    bottom_right_lat=payload['bottom_right_lat'],
                    bottom_right_lng=payload['bottom_right_lng'],
                    question_type=payload['question_type'],
                )
                resp = {'assignment': assignment.to_dict()}
            else:
                self.response.request.status = 400
        else:
            self.response.request.status = 403
        return resp


@view_defaults(route_name='/api/admin/assignments/{id}/responses', renderer='json')
class AdminAssignmentResponsesAPI(object):

    def __init__(self, request):
        self.request = request
        self. user = authenticate(request)
        self.start, self.count = build_paging(request)

    @view_config(request_method='GET')
    def get(self):
        print('\n\n---- responses ----\n\n')  
        resp = {'posts': None}
        if self.user:
            id = self.request.matchdict['id']
            print(id)
            posts = Posts.get_all_by_assignment_id(id)
            print(posts)
            resp = {'posts': [p.to_dict(None) for p in posts]}
        else:
            self.request.response.status = 403
        print('\n\n')
        return resp


@view_defaults(route_name='/api/admin/questions', renderer='json')
class AdminQuestionsAPI(object):

    post_req = (
        'assignment_id',
        'language_code',
        'question_text',
        'description',
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
        if self.user:
            if payload and all(r in payload for r in self.post_req):
                question = Questions.add(
                    user_id=self.user.id,
                    assignment_id=payload['assignment_id'],
                    language_code=payload['language_code'],
                    question_text=payload['question_text'],
                    description=payload['description'],
                    answer0=payload['answer0'],
                    answer1=payload['answer1'],
                    answer2=payload['answer2'],
                    answer3=payload['answer3'],
                    answer4=payload['answer4'],
                )
                resp = {'question': question.to_dict()}
            else:
                self.request.response.status = 400
        else:
            self.request.response.status = 403
        return resp


@view_defaults(route_name='/api/admin/questions/{id}', renderer='json')
class AdminQuestionAPI(object):

    put_req = (
        'language_code',
        'question_text',
        'description',
        'answer0',
        'answer1',
        'answer2',
        'answer3',
        'answer4',
    )

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='PUT')
    def put(self):
        resp = {'question': None}
        payload = get_payload(self.request)
        if self.user:
            if payload and all(r in payload for r in self.put_req):
                question = Questions.get_by_id(self.request.matchdict['id'])
                question = Questions.update_by_id(
                    question.id,
                    user_id=question.user_id,
                    assignment_id=question.assignment_id,
                    language_code=payload['language_code'],
                    question_text=payload['question_text'],
                    description=payload['description'],
                    answer0=payload['answer0'],
                    answer1=payload['answer1'],
                    answer2=payload['answer2'],
                    answer3=payload['answer3'],
                    answer4=payload['answer4'],
                )
                resp = {'question': question.to_dict()}
            else:
                self.request.response.status = 400
        else:
            self.request.response.status = 403
        return resp 


@view_defaults(route_name='/api/admin/users', renderer='json')
class AdminUsersAPI(object):

    post_req = (
        'username',
        'first',
        'last',
        'organization_id',
        'email',
    )    

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='POST')
    def post(self):
        resp = {'user': None}
        payload = get_payload(self.request)
        if self.user:
            if payload and all(r in payload for r in self.post_req):
                user = Users.create_new_user(
                    username=payload['username'],
                    first=payload['first'],
                    last=payload['last'],
                    organization_id=payload['organization_id'],
                    email=payload['email'],            
                )
            else:
                self.request.response.status = 400
        else:
            self.request.response.status = 403
        return resp
        

