import os
import json
from time import strftime
import uuid
import datetime

from utils import make_response, admin_log

import urllib

import transaction

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    UserGeoFences,
    UserTypes,
    Users,
    Assignments,
    Questions,
    QuestionTypes,
    QuestionAssignments,
    Languages,
    Posts,
    MediaTypes,
    MediaObjects,
    PostMediaObjects,
    Stories,
    ClientLogs,
    Collections,
    CollectionPosts,
    Messages,
    Notifications,
    Subscribers,
    )

def check_token(request):
    """ validates token against database """
    valid = False
    user = None
    try:
        token = request.GET['token']
        valid, user = Users.validate_token(DBSession, token)
    except:
        try:
            token = request.session['token']
            valid, user = Users.validate_token(DBSession, token)
        except:
            pass

    return valid, user

@view_config(route_name='admin/get_access_token.json')
def admin_get_access_token(request):

    result = {'success': False}

    try:
    #if True:

        user_name = ''
        password = ''
        try:
            user_name = request.POST['username']
            password = request.POST['password']

        except:
            result['error_text'] = "Missing 'username' or 'password' within request"
            raise Exception('missing credentials')

        user, token = Users.authenticate(DBSession, user_name, password)

        if token == None:
            result['error_text'] = 'Invalid credentials'
            raise Exception('invalid credentials')
        else:

            request.session['token'] = token

            fence = UserGeoFences.get_fence_from_user_id(
                session = DBSession,
                user_id = user.user_id,
            )

            result['token'] = token
            result['username'] = user.user_name
            result['first_name'] = user.first_name
            result['last_name'] = user.last_name
            result['organization'] = user.organization

            result['fence'] = {
                'top_left_lat': fence.top_left_lat,
                'top_left_lng': fence.top_left_lng,
                'bottom_right_lat': fence.bottom_right_lat,
                'bottom_right_lng': fence.bottom_right_lng,
            }

            result['success'] = True

    except Exception, e:
        result['error'] = str(e)

    #admin_log("HTTP: admin/get_access_token.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_client_logs.json')
def admin_get_client_logs(request):

    """
    Returns all of the event logs in the system.  Optionally by client_id.
    """

    result = {'success' :False}

    user = None
    try:
    #if True:
        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        client_id = None
        try:
            client_id = request.GET['client_id']
        except:
            pass

        logs = ClientLogs.get_all(
            session = DBSession
        )

        ret_logs = []
        for log in logs:
            ret_logs.append({
                'client_log_id': log.client_log_id,
                'client_id': log.client_id,
                'url': log.url,
                'lat': log.lat,
                'lng': log.lng,
                'request': log.request,
                'result': log.result,
                'success': log.success,
                'log_datetime': str(log.log_datetime),
            })

        result['logs'] = ret_logs
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_client_logs.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_posts.json')
def admin_get_posts(request):

    """ Will return current posts from database """

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        start = 0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count = 0
        try:
            count = int(request.GET['count'])
        except:
            pass

        deleted = False
        try:
            deleted = bool(int(request.GET['deleted']))
        except:
            pass

        posts, total_post_count = Posts.get_posts(
            DBSession,
            deleted = deleted,
            start = start,
            count = count,
        )

        ret_posts = []

        if total_post_count != 0 and len(posts) > 0 and posts[0][0] != None:

            seen_post_ids = []
            post = {}

            # itterate throught he list, and build our resposne
            index = 0
            for post_id, user_id, post_datetime, deleted, \
                    lat, lng, media_object_id, media_id, file_name, \
                    caption, media_text, media_type_name, \
                    media_type_description, verified, client_id, \
                    language_code, language_name, assignment_id, \
                    assignment_name in posts:

                if (post_id not in seen_post_ids) or (index == len(posts)-1):

                    if post:

                        ret_posts.append(post)

                    post = {
                        'post_id': post_id,
                        'user_id': user_id,
                        #'title': title,
                        'post_datetime': str(post_datetime),
                        'deleted': deleted,
                        'lat': lat,
                        'lng': lng,
                        'verified_user': bool(verified),
                        'client_id': client_id,
                        'language_code': language_code,
                        'language_name': language_name,
                        'assignment_id': assignment_id,
                        'assignment_name': assignment_name,
                        'media_objects': []
                    }

                    seen_post_ids.append(post_id)
                
                preview_file_name = ''
                if not file_name == "":
                    root_file_name = os.path.splitext(file_name)[0]
                    file_extention = os.path.splitext(file_name)[1]
                    preview_file_name = "{0}p{1}".format(root_file_name,file_extention)
                media_object = {
                    'media_id': media_id,
                    'file_name': file_name,
                    'preview_file_name': preview_file_name,
                    'caption': caption,
                    'media_text': media_text,
                    'media_type_name': media_type_name,
                    'media_type_description': media_type_description,
                }

                post['media_objects'].append(media_object)

                if index == len(posts)-1:
                    ret_posts.append(post)

                index += 1

        result['total_post_count'] = total_post_count
        result['posts'] = ret_posts

        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_posts.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/create_question.json')
def admin_create_question(request):

    result = {'success': False}

    #if True:
    try:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        #if True:
        try:
            language_code = request.POST['language_code']
            question_text = request.POST['question_text']
            description = request.POST['description']
            question_type = request.POST['question_type']

            result['language_code'] = language_code
            result['question_text'] = question_text
            result['description'] = description
            result['question_type'] = question_type

        except:
            result['error_text'] = "Missing field"
            raise Exception('missing field')

        # answers is a json array of strings
        answers = []
        try:
        #if True:
            answers = json.loads(request.POST['answers'])
        except:
            pass

        result['answers'] = answers

        # back fill with empty strings
        for i in range(len(answers),10):
            answers.append('')

        question = Questions.create_from_http(
            session = DBSession,
            token = user.token,
            language_code = language_code,
            question_text = question_text,
            description = description,
            question_type = question_type,
            answers = answers,
        )

        result['question_id'] = question.question_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/create_question.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/update_question.json')
def admin_update_question(request):

    result = {'success': False}

    #if True:
    try:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        #if True:
        try:
            language_code = request.POST['language_code']
            question_text = request.POST['question_text']
            description = request.POST['description']
            question_type = request.POST['question_type']
        except:
            result['error_text'] = "Missing field"
            raise Exception('missing field')

        # answers is a json array of strings
        answers = []
        try:
        #if True:
            answers = json.loads(request.POST['answers'])
        except:
            pass
        # back fill with empty strings
        for i in range(len(answers),10):
            answers.append('')

        question = Questions.update_from_http(
            session = DBSession,
            token = user.token,
            language_code = language_code,
            question_text = question_text,
            description = description,
            question_type = question_type,
            answers = answers,
        )

        result['question_id'] = question.question_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/updatequestion.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/publish_assignment.json')
def admin_publish_assignment(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        #if True:
        try:
            name = request.POST['name']
            life_time = 0
            try:
                life_time = int(float(request.POST['life_time']))
            except:
                pass
            if life_time == 0:
                life_time = 168 # set to 1 week if blank
            questions = json.loads(request.POST['questions'])
            if request.POST['top_left_lat'] == "" or \
                    request.POST['top_left_lng'] == "" or \
                    request.POST['bottom_right_lat'] == "" or \
                    request.POST['bottom_right_lng'] == "":
                top_left_lat = 43.4
                top_left_lng = -77.9
                bottom_right_lat = 43.0
                bottom_right_lng = -77.1
            else:
                top_left_lat = float(request.POST['top_left_lat'])
                top_left_lng = float(request.POST['top_left_lng'])
                bottom_right_lat = float(request.POST['bottom_right_lat'])
                bottom_right_lng = float(request.POST['bottom_right_lng'])

            result['name'] = name
            result['life_time'] = life_time
            result['questions'] = questions
            result['top_left_lat'] = top_left_lat
            result['top_left_lng'] = top_left_lng
            result['bottom_right_lat'] = bottom_right_lat
            result['bottom_right_lng'] = bottom_right_lng

        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        #geo_fence = {
        #    'top_left_lat': top_left_lat,
        #    'top_left_lng': top_left_lng,
        #    'bottom_right_lat': bottom_right_lat,
        #    'bottom_right_lng': bottom_right_lng,
        #}

        # create assignment
        assignment = Assignments.create_from_http(
            session = DBSession,
            token = user.token,
            name = name,
            life_time = life_time,
            #geo_fence = geo_fence,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
        )

        collection = Collections.create_new_collection_from_http(
            session = DBSession,
            token = user.token,
            name = "{0} (Assignment #{1})".format(name, assignment.assignment_id),
            description = "",
            tags = "",
        )

        Assignments.set_collection(
            session = DBSession,
            assignment_id = assignment.assignment_id,
            collection_id = collection.collection_id,
        )

        # assign question to assignment
        for question_id in questions:
            QuestionAssignments.create(
                DBSession,
                assignment.assignment_id,
                question_id,
            )

        result['assignment_id'] = assignment.assignment_id
        result['question_ids'] = questions
        result['collection_id'] = collection.collection_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/publish_assignment.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/update_assignment.json')
def admin_update_assignment(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        #if True:
        try:
            assignment_id = request.POST['assignment_id']
            #client_id = request.POST['client_id']
            name = request.POST['name']
            life_time = 0
            try:
                life_time = int(float(request.POST['life_time']))
            except:
                life_time = 24*7
            #questions = json.loads(request.POST['questions'])
            top_left_lat = float(request.POST['top_left_lat'])
            top_left_lng = float(request.POST['top_left_lng'])
            bottom_right_lat = float(request.POST['bottom_right_lat'])
            bottom_right_lng = float(request.POST['bottom_right_lng'])
            #use_fence = boolean(request.POST['use_fence'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        # create assignment
        assignment = Assignments.update_assignment(
            session = DBSession,
            assignment_id = assignment_id,
            name = name,
            life_time = life_time,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
            #use_fence = use_fence,
        )

        result['assignment_id'] = assignment.assignment_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/update_assignment.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_assignments.json')
def admin_get_my_assignments(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token what ...')

        start=0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count=50
        try:
            count = int(request.GET['count'])
        except:
            pass

        assignments,assignment_count = Assignments.get_all_with_questions_from_token(
            session = DBSession,
            token = user.token,
            start = start,
            count = count,
        )

        #print "\n\nASSIGNMENTS:\n\n"
        #print assignments
        #print "\n\n"

        ret_assignments = []
        # this is for development.ini ... sqlite was puking on the query
        if assignment_count != 0 and len(assignments) > 0 and assignments[0][0] != None:


            seen_assignment_ids = []
            assignment = {}

            # itterate throught he list, and build our resposne
            index = 0
            for assignment_id, publish_datetime, expire_datetime, name, \
                    top_left_lat, top_left_lng, bottom_right_lat, \
                    bottom_right_lng, use_fence, collection_id, organization, \
                    question_text, question_type_id, question_description, \
                    answer0, answer1, answer2, answer3, answer4, answer5, \
                    answer6, answer7, answer8, answer9, post_count \
                    in assignments:

                if (assignment_id not in seen_assignment_ids) or (index == len(assignments)-1):

                    # add our existing assignment to the list of assignments
                    # to return
                    if assignment:
                        ret_assignments.append(assignment)

                    # build our assignment with no question(s)
                    assignment = {
                        'assignment_id': assignment_id,
                        'publish_datetime': str(publish_datetime),
                        'expire_datetime': str(expire_datetime),
                        'name': name,
                        'top_left_lat': top_left_lat,
                        'top_left_lng': top_left_lng,
                        'bottom_right_lat': bottom_right_lat,
                        'bottom_right_lng': bottom_right_lng,
                        #'use_fence': use_fence,
                        'organization': organization,
                        'questions': [],
                        'post_count': post_count,
                    }

                    # record that we have seen the assignment_id
                    seen_assignment_ids.append(assignment_id)

                # build our question
                question = {
                    'question_text': question_text,
                    'question_type_id': question_type_id,
                    'description': question_description,
                    'answer0': answer0,
                    'answer1': answer1,
                    'answer2': answer2,
                    'answer3': answer3,
                    'answer4': answer4,
                    'answer5': answer5,
                    'answer6': answer6,
                    'answer7': answer7,
                    'answer8': answer8,
                    'answer9': answer9,
                }

                # add the question to the current assignment
                assignment['questions'].append(question)

                if index == len(assignments)-1:
                    ret_assignments.append(assignment)

                index += 1

        result['assignment_count'] = assignment_count
        result['assignments'] = ret_assignments
        result['success'] = True

    except:
        pass

    admin_log("HTTP: admin/get_my_assignments.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/create_message.json')
def admin_create_message(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
            to_client_id = request.POST['to_client_id']
            subject = request.POST['subject']
            text = request.POST['text']
        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        parent_message_id = None
        try:
            parent_message_id = request.POST['parent_message_id']
        except:
            pass

        message = Messages.create_message_from_http(
            session = DBSession,
            from_token = user.token,
            to_client_id = to_client_id,
            subject = subject,
            text = text,
            parent_message_id = parent_message_id,
        )

        if message != None:
            result['message_id'] = message.message_id
            result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/create_message.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_my_messages.json')
def admin_get_my_messages(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        user = Users.get_from_token(DBSession, token)
        messages = Messages.get_messages_from_client_id(
            DBSession,
            user.client_id,
        )
        ret_messages = []
        for message_id, from_user_id,to_user_id,message_datetime, \
                parent_message_id,subject,text, was_read,from_organization, \
                from_first_name,from_last_name in messages:
            ret_messages.append({
                'message_id': message_id,
                'from_user_id': from_user_id,
                'to_user_id': to_user_id,
                'from_organization': from_organization,
                'from_first_name': from_first_name,
                'from_last_name': from_last_name,
                'message_datetime': str(message_datetime),
                'parent_message_id': parent_message_id,
                'subject': subject,
                'text': text,
                'was_read': was_read,
            })

        result['messages'] = ret_messages
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_my_messages.json => {0}".format(json.dumps(result)))

    return make_response(result)


@view_config(route_name='admin/get_languages.json')
def admin_get_languages(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        languages = Languages.get_all(DBSession)

        ret_languages = []
        for language_code, name in languages:
            ret_languages.append({
                'name': name,
                'code': language_code,
            })

        result['languages'] = ret_languages
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_languages.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_question_types.json')
def admin_get_question_types(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        question_types = QuestionTypes.get_all(DBSession)

        ret_question_types = []
        for question_type_id, question_type_text, question_type_description \
                in question_types:
            ret_question_types.append({
                'question_type_id': question_type_id,
                'question_type_text': question_type_text,
                'question_type_description': question_type_description,
            })

        result['question_types'] = ret_question_types
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_question_types.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_assignment_responses.json')
def admin_get_assignment_responses(request):

    result = {'success': False}

    try:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
            assignment_id = int(request.GET['assignment_id'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        start=0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count=0
        try:
            count = int(request.GET['count'])
        except:
            pass

        deleted=False
        try:
            deleted = bool(int(request.GET['deleted'])) 
        except:
            pass

        posts,post_count = Posts.get_all_from_assignment_id(
            session = DBSession,
            assignment_id = assignment_id,
            deleted = deleted,
            start = start,
            count = count,
        )

        ret_posts = []

        if post_count != 0 and len(posts) > 0 and posts[0][0] != None:

            seen_post_ids = []
            post = {}

            # itterate throught he list, and build our resposne
            index = 0
            for post_id, assignment_id, client_id, post_datetime, \
                    deleted, lat, lng, media_object_id, media_id, \
                    file_name, caption, media_text, media_type_name, \
                    media_type_description, verified, client_id, \
                    language_code, language_name in posts:

                if (post_id not in seen_post_ids) or (index == len(posts)-1):

                    if post:

                        ret_posts.append(post)

                    post = {
                        'post_id': post_id,
                        'assignment_id': assignment_id,
                        'client_id': client_id,
                        #'title': title,
                        'post_datetime': str(post_datetime),
                        'deleted': deleted,
                        'lat': lat,
                        'lng': lng,
                        'verified_user': bool(verified),
                        'client_id': client_id,
                        'language_code': language_code,
                        'language_name': language_name,
                        'media_objects': []
                    }

                    seen_post_ids.append(post_id)

                preview_file_name = ''
                if not file_name == "":
                    root_file_name = os.path.splitext(file_name)[0]
                    file_extention = os.path.splitext(file_name)[1]
                    preview_file_name = "{0}p{1}".format(root_file_name,file_extention)
                media_object = {
                    'media_id': media_id,
                    'file_name': file_name,
                    'preview_file_name': preview_file_name,
                    'caption': caption,
                    'media_text': media_text,
                    'media_type_name': media_type_name,
                    'media_type_description': media_type_description,
                }

                post['media_objects'].append(media_object)

                if index == len(posts)-1:
                    ret_posts.append(post)

                index += 1

        result['post_count'] = post_count
        result['posts'] = ret_posts
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_assignment_responses.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/register_post_view.json')
def admin_register_post_view(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
            post_id = request.POST['post_id']
        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        post = Posts.get_from_post_id(
            session = DBSession,
            post_id = post_id,
        )

        notification = Notifications.create_notification(
            session = DBSession,
            user_id = post.user_id,
            notification_type = 'post_viewed',
            payload = json.dumps({
                'organization': user.organization,
            })
        )

        result['post_id'] = post_id
        result['notification_id'] = notification.notification_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/register_post_view.json => {0}".format(json.dumps(result)))

    return make_response(result)


@view_config(route_name='admin/publish_story.json')
def admin_publish_story(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
            title = request.POST['title']
            tags = request.POST['tags']
            top_text = request.POST['top_text']
            banner_media_id = request.POST['banner_media_id']
            contents = request.POST['contents'].encode('UTF-8')
            top_left_lat = float(request.POST['top_left_lat'])
            top_left_lng = float(request.POST['top_left_lng'])
            bottom_right_lat = float(request.POST['bottom_right_lat'])
            bottom_right_lng = float(request.POST['bottom_right_lng'])
            language_code = request.POST['language_code']
            #use_fense = request.POST['use_fense']
        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        story = Stories.create_from_http(
            session = DBSession,
            token = user.token,
            title = title,
            tags = tags,
            top_text = top_text,
            media_id = banner_media_id,
            contents = contents,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
            #use_fence = use_fense,
            language_code = language_code,
        )

        result['story_unique_id'] = story.story_unique_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/publish_story.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_my_collections.json')
def admin_get_my_collection(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        collections = Collections.get_all_from_http(
           session = DBSession,
           token = user.token,
        )

        ret_collections = []
        for collection_id, user_id, collection_datetime, name, description, \
                tags, enabled, assignment_id, assignment_name, post_count \
                in collections:
            ret_collections.append({
                'collection_id': collection_id,
                'collection_datetime': str(collection_datetime),
                'name': name,
                'decription': description,
                'tags': tags,
                'enabled': enabled,
                'assignment_id': assignment_id,
                'assignment_name': assignment_name,
                'post_count': post_count,
            })

        result['collections'] = ret_collections
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_my_collections.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/create_collection.json')
def admin_create_collection(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
        #if True:
            name = request.POST['name']
            description = request.POST['description']
            tags = request.POST['tags']
        except:
            result['error_text'] = "Missing field"
            raise Exception('Missing or invalid field.')

        collection = Collections.create_new_collection_from_http(
            session = DBSession,
            token = user.token,
            name = name,
            description = description,
            tags = tags,
        )

        result['collection_id'] = collection.collection_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/create_collection.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/add_post_to_collection.json')
def admin_add_post_to_collection(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
        #if True:
            collection_id = int(request.POST['collection_id'])
            post_id = int(request.POST['post_id'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('Missing or invalid field.')

        _collection = Collections.get_from_collection_id(
            session = DBSession,
            collection_id = collection_id,
        )

        _post = Posts.get_from_post_id(
            session = DBSession,
            post_id = post_id,
        )

        if _collection == None or _post == None:
            result['error_test'] = "Invalid collection or post id"
            raise Exception("Invalid collection or post id");

        collection_post = Collections.add_post_to_collection(
            session = DBSession,
            collection_id = collection_id,
            post_id = post_id,
        )

        result['post_id'] = collection_post.post_id
        result['collection_id'] = collection_post.collection_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/add_post_to_collection.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/remove_post_from_collection.json')
def admin_remove_post_from_collection(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
        #if True:
            collection_id = int(request.POST['collection_id'])
            post_id = int(request.POST['post_id'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('Missing or invalid field.')

        successfully_removed = Collections.remove_post_from_collection(
            session = DBSession,
            collection_id = collection_id,
            post_id = post_id,
        )
        if successfully_removed:
            result['post_id'] = post_id
            result['collection_id'] = collection_id
            result['success'] = True
        else:
            result['error_text'] = 'Post does not exist within collection.'

    except:
        pass

    #admin_log("HTTP: admin/remove_post_from_collection.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/disable_collection.json')
def admin_disable_collection(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
        #if True:
            collection_id = int(request.POST['collection_id'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('Missing or invalid field.')

        collection = Collections.disable_collection(
            session = DBSession,
            collection_id = collection_id,
        )

        result['collection_id'] = collection.collection_id
        result['disabled'] = True
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/disable_collection.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_collection_posts.json')
def admin_get_collection_posts(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
            collection_id = int(request.GET['collection_id'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        start=0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count=0
        try:
            count = int(request.GET['count'])
        except:
            pass

        posts,post_count = Posts.get_all_from_collection_id(
            session = DBSession,
            collection_id = collection_id,
            start = start,
            count = count,
        )
        collection = Collections.get_from_collection_id(
            session = DBSession,
            collection_id = collection_id,
        )

        ret_posts = []

        if post_count != 0 and len(posts) > 0 and posts[0][0] != None:

            seen_post_ids = []
            post = {}

            # itterate throught he list, and build our resposne
            index = 0
            for post_id, assignment_id, user_id, post_datetime, \
                    deleted, lat, lng, media_object_id, media_id, \
                    file_name, caption, media_text, media_type_name, \
                    media_type_description, verified, client_id, \
                    language_code, language_name in posts:

                if (post_id not in seen_post_ids) or (index == len(posts)-1):

                    if post:

                        ret_posts.append(post)

                    post = {
                        'post_id': post_id,
                        'assignment_id': assignment_id,
                        'user_id': user_id,
                        #'title': title,
                        'post_datetime': str(post_datetime),
                        'deleted': deleted,
                        'lat': lat,
                        'lng': lng,
                        'verified_user': bool(verified),
                        'client_id': client_id,
                        'language_code': language_code,
                        'language_name': language_name,
                        'media_objects': []
                    }

                    seen_post_ids.append(post_id)

                preview_file_name = ''
                if not file_name == "":
                    root_file_name = os.path.splitext(file_name)[0]
                    file_extention = os.path.splitext(file_name)[1]
                    preview_file_name = "{0}p{1}".format(root_file_name,file_extention)
                media_object = {
                    'media_id': media_id,
                    'file_name': file_name,
                    'preview_file_name': preview_file_name,
                    'caption': caption,
                    'media_text': media_text,
                    'media_type_name': media_type_name,
                    'media_type_description': media_type_description,
                }

                post['media_objects'].append(media_object)

                if index == len(posts)-1:
                    ret_posts.append(post)

                index += 1

        result['post_count'] = post_count
        result['collection_id'] = collection.collection_id
        result['collection_name'] = collection.name
        result['posts'] = ret_posts
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_collection_posts.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_user_posts.json')
def admin_get_user_posts(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
        #if True:
            #
            # TODO: convert this over from client_id to cuid
            #
            client_id = request.GET['client_id']

            cuid = client_id

        except:
            result['error_text'] = "Missing field"
            raise Exception('Missing or invalid field.')

        start=0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count=0
        try:
            count = int(request.GET['count'])
        except:
            pass

        posts,post_count = Posts.get_all_from_cuid(
            session = DBSession,
            cuid = cuid,
            start = start,
            count = count,
        )

        ret_posts = []

        if post_count != 0 and len(posts) > 0 and posts[0][0] != None:

            seen_post_ids = []
            post = {}

            # itterate throught he list, and build our resposne
            index = 0
            for post_id, assignment_id, user_id, post_datetime, \
                    deleted, lat, lng, media_object_id, media_id, \
                    file_name, caption, media_text, media_type_name, \
                    media_type_description, verified, client_id, \
                    language_code, language_name in posts:

                if (post_id not in seen_post_ids) or (index == len(posts)-1):

                    if post:

                        ret_posts.append(post)

                    post = {
                        'post_id': post_id,
                        'assignment_id': assignment_id,
                        'user_id': user_id,
                        #'title': title,
                        'post_datetime': str(post_datetime),
                        'deleted': deleted,
                        'lat': lat,
                        'lng': lng,
                        'verified_user': bool(verified),
                        'client_id': client_id,
                        'language_code': language_code,
                        'language_name': language_name,
                        'media_objects': []
                    }

                    seen_post_ids.append(post_id)

                preview_file_name = ''
                if not file_name == "":
                    root_file_name = os.path.splitext(file_name)[0]
                    file_extention = os.path.splitext(file_name)[1]
                    preview_file_name = "{0}p{1}".format(root_file_name,file_extention)
                media_object = {
                    'media_id': media_id,
                    'file_name': file_name,
                    'preview_file_name': preview_file_name,
                    'caption': caption,
                    'media_text': media_text,
                    'media_type_name': media_type_name,
                    'media_type_description': media_type_description,
                }

                post['media_objects'].append(media_object)

                if index == len(posts)-1:
                    ret_posts.append(post)

                index += 1

        result['post_count'] = post_count
        result['posts'] = ret_posts
        result['client_id'] = client_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_user_posts.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_subscriber_list.json')
def admin_get_subscriber_list(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        subscribers = Subscribers.get_all_subscribers(
            session = DBSession,
        )

        ret_subscribers = []
        for email,subscribe_datetime,name,organization, \
                profession,receive_updates,receive_version_announcement, \
                interested_in_partnering,want_to_know_more in subscribers:
            ret_subscribers.append({
                'email': email,
                'subscribe_datetime': str(subscribe_datetime),
                'name': name,
                'organization': organization,
                'profession': profession,
                'receieve_updates': receieve_updates,
                'receieve_version_announcement': receieve_version_announcement,
                'interested_in_partnering': interested_in_partnering,
                'want_to_know_more': want_to_know_more,
            })

        result['subscribers'] = ret_subscribers
        result['success'] = True

    except:
        pass

    return make_response(result)

@view_config(route_name='admin/create_user.json')
def admin_create_user(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
        #if True:
            user_type_id = request.POST['user_type_id']
            #client_id = request.POST['client_id']
            user_name = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            organization = request.POST['organization']
            fence_top_left_lat = float(request.POST['fence_top_left_lat'])
            fence_top_left_lng = float(request.POST['fence_top_left_lng'])
            fence_bottom_right_lat = float(request.POST['fence_bottom_right_lat'])
            fence_bottom_right_lng = float(request.POST['fence_bottom_right_lng'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('Missing or invalid field.')

        # we need to make sure that the user trying to create the
        # new user has the right access level
        system_user_type = UserTypes.get_from_name(
            session = DBSession,
            name = 'system',
        )
        admin_user_type = UserTypes.get_from_name(
            session = DBSession,
            name = 'admin',
        )
        moderator_user_type = UserTypes.get_from_name(
            session = DBSession,
            name = 'moderator',
        )

        new_user_id = None

        if user.user_type_id == system_user_type.user_type_id or \
                user.user_type_id == admin_user_type.user_type_id or \
                user.user_type_id == moderator_user_type.user_type_id:

            user_geo_fence = UserGeoFences.create_fence(
                session = DBSession,
                top_left_lat = fence_top_left_lat,
                top_left_lng = fence_top_left_lng,
                bottom_right_lat = fence_bottom_right_lat,
                bottom_right_lng = fence_bottom_right_lng,
            )

            new_user = Users.create_new_user(
                session = DBSession,
                user_type_id = user_type_id,
                user_geo_fence_id = user_geo_fence.user_geo_fence_id,
                user_name = user_name,
                password = password,
                first_name = first_name,
                last_name = last_name,
                email = email,
                organization = organization,
                #client_id = client_id,
            )

            new_user_id = new_user.user_id

            #verified_new_user = Users.verify_user(
            #    session = DBSession,
            #    client_id = new_user.client_id,
            #    user_name = user_name,
            #    password = password,
            #    first_name = first_name,
            #    last_name = last_name,
            #    email = email,
            #)

            #new_user_id = verified_new_user.user_id


        result['user_id'] = new_user_id
        #result['disabled'] = True
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_subscriber_list.json => {0}".format(json.dumps(result)))

    return make_response(result)

@view_config(route_name='admin/get_post.json')
def admin_get_post(request):

    result = {'success': False}

    try:
    #if True:
        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
        #if True:
            post_id = request.GET['post_id']
        except:
            result['error_text'] = "Missing fields"
            raise Exception('missing post_id') 

        posts, post_count = Posts.get_with_media_objects_from_post_id(
            session = DBSession,
            post_id = post_id,
        )

        ret_posts = []

        if post_count != 0 and len(posts) > 0 and posts[0][0] != None:

            seen_post_ids = []
            post = {}

            # itterate throught he list, and build our resposne
            index = 0
            for post_id, assignment_id, user_id, post_datetime, \
                    deleted, lat, lng, media_object_id, media_id, \
                    file_name, caption, media_text, media_type_name, \
                    media_type_description, verified, client_id, \
                    language_code, language_name in posts:

                if (post_id not in seen_post_ids) or (index == len(posts)-1):

                    if post:

                        ret_posts.append(post)

                    post = {
                        'post_id': post_id,
                        'assignment_id': assignment_id,
                        'user_id': user_id,
                        #'title': title,
                        'post_datetime': str(post_datetime),
                        'deleted': deleted,
                        'lat': lat,
                        'lng': lng,
                        'verified_user': bool(verified),
                        'client_id': client_id,
                        'language_code': language_code,
                        'language_name': language_name,
                        'media_objects': []
                    }

                    seen_post_ids.append(post_id)

                preview_file_name = ''
                if not file_name == "":
                    root_file_name = os.path.splitext(file_name)[0]
                    file_extention = os.path.splitext(file_name)[1]
                    preview_file_name = "{0}p{1}".format(root_file_name,file_extention)
                media_object = {
                    'media_id': media_id,
                    'file_name': file_name,
                    'preview_file_name': preview_file_name,
                    'caption': caption,
                    'media_text': media_text,
                    'media_type_name': media_type_name,
                    'media_type_description': media_type_description,
                }

                post['media_objects'].append(media_object)

                if index == len(posts)-1:
                    ret_posts.append(post)

                index += 1
 
        result['post'] = ret_posts[0]
        result['success'] = True

    except:
        pass

    return make_response(result)

@view_config(route_name='admin/delete_post.json')
def admin_delete_post(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
            post_id = request.POST['post_id']
        except:
            result['error_text'] = "Missing fields"
            raise Exception('invalid/missing field')

        post = Posts.delete_post(
            session = DBSession,
            post_id = post_id,
        )

        #notification = Notifications.create_notification(
        #    session = DBSession,
        #    client_id = post.client_id,
        #    notification_type = 'post_deleted',
        #    payload = json.dumps({
        #        'organization': user.organization,
        #    })
        #)

        result['post_id'] = post.post_id
        #result['notification_id'] = notification.notification_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/delete_post.json => {0}".format(json.dumps(result)))

    return make_response(result)

