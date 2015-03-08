import os
import json
from time import strftime
import uuid
import datetime

from utils import make_response, admin_log

import admin_utils

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
        valid, user = admin_utils.check_token(request)
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

@view_config(route_name='admin/create_question.json')
def admin_create_question(request):

    result = {'success': False}

    #if True:
    try:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
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
            user_id = user.user_id,
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
        valid, user = admin_utils.check_token(request)
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
        valid, user = admin_utils.check_token(request)
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
            user_id = user.user_id,
            name = name,
            life_time = life_time,
            #geo_fence = geo_fence,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
        )

        collection = Collections.create_new_collection( #_from_http(
            session = DBSession,
            user_id = user.user_id,
            name = name, #"{0} (A)".format(name), #, assignment.assignment_id),
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
        valid, user = admin_utils.check_token(request)
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

@view_config(route_name='admin/create_message.json')
def admin_create_message(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
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

@view_config(route_name='admin/register_post_view.json')
def admin_register_post_view(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
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
        valid, user = admin_utils.check_token(request)
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

@view_config(route_name='admin/create_collection.json')
def admin_create_collection(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
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

        collection = Collections.create_new_collection( #_from_http(
            session = DBSession,
            user_id = user.user_id,
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
        valid, user = admin_utils.check_token(request)
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
        valid, user = admin_utils.check_token(request)
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
        valid, user = admin_utils.check_token(request)
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

@view_config(route_name='admin/get_subscriber_list.json')
def admin_get_subscriber_list(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
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
        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
        #if True:
            user_type_name = request.POST['user_type']
            #client_id = request.POST['client_id']
            user_name = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            #organization = request.POST['organization']
            organization_id = request.POST['organization_id']
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

        user_type = UserTypes.get_from_name(
            session = DBSession,
            name = user_type_name,
        )

        if user_type == None:
            result['error_text'] = "Invalid user_type"
            raise Exception("Invalid user_type")

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
                user_type_id = user_type.user_type_id,
                user_geo_fence_id = user_geo_fence.user_geo_fence_id,
                user_name = user_name,
                password = password,
                first_name = first_name,
                last_name = last_name,
                email = email,
                #organization = organization,
                organization_id = organization_id,
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

@view_config(route_name='admin/delete_post.json')
def admin_delete_post(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
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

