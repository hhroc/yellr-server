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
    user = None
    token = None
    try:
        #print('session items:')
        #print(request.session.items())
        token = request.session['token']
        #print('\n\n\nToken: ' + token)
    except:
        #print('\n\n\nBAD TOKEN')
        pass
    print('autheticate() Token: ' + str(token))
    if token:
        user = Users.get_by_token(token)
    return user
    

@view_defaults(route_name='/api/admin/login', renderer='json')
class AdminLoginAPI(object):

    post_req = (
        'username',
        'password',
    )

    def __init__(self, request):
        print('/api/admin/login')
        self.request = request
        #DBSession.commit()
        self.user = authenticate(request)

    @view_config(request_method='GET')
    def get(self):
        print('---- start [GET] /api/admin/login')
        resp = {'loggedin': False}
        #print('\nToken:' + self.request.session['token'] if 'token' in self.request.session else None)
        #print('\n\n')
        #print([u.to_dict() for u in Users.get_all()])
        #print('\n\n')
        #for u in Users.get_all():
        #    DBSession.refresh(u)
        #print('\n\n')
        #print([u.to_dict() for u in Users.get_all()])
        #print('\n\n')
        if self.user:
            resp = {'loggedin': True}
        #else:
            #self.request.response.status = 403
        #if self.user:
        #    DBSession.expire(self.user)
        print('---- end [GET] /api/admin/login')
        return resp
        
    @view_config(request_method='POST')
    def post(self):
        print('---- start [POST] /api/admin/login')
        resp = {'user': None}
        payload = get_payload(self.request)
        if payload and all(r in payload for r in self.post_req):
            user = Users.authenticate(
                username=payload['username'],
                password=payload['password'],
            )
            resp = {'user': user.to_dict()}
            self.request.session['token'] = user.token
            if user.token is None:
                raise Exception('user token is None after login')
            #print('\n\nLogin Token:')
            #print(user.token)
            #print(self.request.session['token'])
        #else:
        #    self.request.response.status = 403
        #if self.user:
        #    DBSession.expire(self.user)
        print('---- end [POST] /api/admin/login')
        return resp


@view_defaults(route_name='/api/admin/logout', renderer='json')
class AdminLogoutAPI(object):

    def __init__(self, request):
        print('/api/admin/logout')
        self.request = request
        #DBSession.commit()
        self.user = authenticate(request)

    @view_config(request_method='POST')
    def post(self):
        print('---- start [POST] /api/admin/logout')
        resp = {'user': None}
        token = self.request.session['token']
        if token:
            user = Users.invalidate_token(token)
            if user:
                resp = {'user': user.to_dict()}
            else:
                self.request.response.stats = 403
        #if self.user:
        #    DBSession.expire(self.user)
        print('---- end /api/admin/logout')
        return resp    

'''
@view_defaults(route_name='/api/admin/loggedin', renderer='json')
class AdminLoggedinAPI(object):

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='GET')
    def get(self):
        resp = {'loggedin': False}
        if self.user:
            resp = {'loggedin': True}
        else:
            self.request.response.status = 403
        return resp
'''

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
            #collection = Collections.add(
            #    user_id=self.user.id,
            #    name=payload['name'],
            #    description='Collection for Assignment: ' + payload['name'],
            #    tags='',
            #    enabled=True,
            #)
            assignment = Assignments.add(
                user_id=self.user.id,
                expire_datetime=datetime.datetime.now() + timedelta(hours=float(payload['life_time'])),
                name=payload['name'],
                top_left_lat=payload['top_left_lat'],
                top_left_lng=payload['top_left_lng'],
                bottom_right_lat=payload['bottom_right_lat'],
                bottom_right_lng=payload['bottom_right_lng'],
                #collection_id=collection.id,
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
        if self.user and payload and all(r in payload for r in self.post_req):
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
        if self.user and payload and all(r in payload for r in self.put_req):
            question = Questions.get_by_id(self.request.matchdict['id'])
            question = Questions.update_by_id(
                question.id,
                user_id=question.user_id,
                assignment_id=question.assignment_id,
                language_code=payload['language_code'],
                question_text=payload['question_text'],
                description=payload['description'],
                question_type=question.question_type,
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

@view_defaults(route_name='/api/admin/users', renderer='json')
class AdminUsersAPI(object):

    

    def __init__(self, request):
        self.request = request
        self.user = authenticate(request)

    @view_config(request_method='POST')
    def post(self):
        resp = {'user': None}
        payload = get_payload(self.request)
        if self.user and payload and all(r in payload for r in self.post_req):
            user = Users.create_new_user(
                username=payload['username'],
                first=payload['first'],
                last=payload['last'],
                organization_id=payload['organization_id'],
                email=payload['email'],
                
            )
        else:
            self.request.response.status = 400
        

