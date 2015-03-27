import json
import datetime
import os

import markdown

import utils

from pyramid.response import Response

from .models import (
    DBSession,
    UserTypes,
    Users,
    Clients,
    Assignments,
    Questions,
    QuestionAssignments,
    QuestionTypes,
    Languages,
    Posts,
    #MediaTypes,
    #MediaObjects,
    #PostMediaObjects,
    Stories,
    #ClientLogs,
    Collections,
    #CollectionPosts,
    Messages,
    Notifications,
    UserGeoFences,
    Organizations,
)

def check_token(request):
    """ validates token against database """
    valid = False
    user = None

    #print "\n\nREQUEST.GET:"
    #print request.GET
    #print "\n\nREQUEST.POST:"
    #print request.POST
    #print "\n\nREQUEST.SESSION:"
    #print request.session

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

def check_logged_in(request):

    valid, user = check_token(request)

    org = None
    fence = None
    if valid is True:
       org = Organizations.get_from_id(
           session = DBSession,
           organization_id = user.organization_id,
       )
       fence = UserGeoFences.get_fence_from_user_id(
           session = DBSession,
           user_id = user.user_id,
       )

    return valid, user, org, fence

def authenticate(username, password):
    user = None
    token = None
    fence = None
    org = None

    try:
    
        user, org, token = Users.authenticate(DBSession, username, password)

        # make sure the user is valid, and is so, get their geofence
        if token is not None:
            fence = UserGeoFences.get_fence_from_user_id(
                session = DBSession,
                user_id = user.user_id,
            )

    except:
        raise Exception("Database error.")

    return user, org, token, fence

def logout(token):

    user = None

    try:

        user = Users.invalidate_token(
            session = DBSession,
            token = token,
        )

    except:
        raise Exception("Database error.")

    return user

def check_super_user(user_type_id):

    is_super_user = False
    
    try:

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

        is_super_user = False
        if user_type_id == system_user_type.user_type_id or \
                user_type_id == admin_user_type.user_type_id or \
                user_type_id == moderator_user_type.user_type_id:
            is_super_user = True

    except:
        raise Exception("Database error.")

    return is_super_user

def create_user(user_type_id, user_type_name, user_name, password, first_name,\
         last_name, email, organization_id, top_left_lat, top_left_lng,\
         bottom_right_lat, bottom_right_lng):

    new_user = None

    try:

        user_type = UserTypes.get_from_name(
            session = DBSession,
            name = user_type_name,
        )

        new_user = None
        if user_type is not None and check_super_user(user_type_id) is True:
            user_geo_fence = UserGeoFences.create_fence(
                session = DBSession,
                top_left_lat = top_left_lat,
                top_left_lng = top_left_lng,
                bottom_right_lat = bottom_right_lat,
                bottom_right_lng = bottom_right_lng,
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
                organization_id = organization_id,
            )

    except:
        raise Exception("Database error.")

    return new_user

def change_password(username, old_password, new_password):

    user = None
    success = False
    
    try:

        user,success = Users.change_password(
            session = DBSession,
            username = username,
            old_password = old_password,
            new_password = new_password,
        )

    except:
        raise Exception("Database error.")

    return user,success

def get_languages():

    ret_languages = []
    
    try:

        languages = Languages.get_all(
            session = DBSession
        )

        ret_languages = utils._decode_languages(languages)

    except:
        raise Exception("Database error.")

    return ret_languages

def get_question_types():

    ret_question_types = []

    try:

        question_types = QuestionTypes.get_all(
            session = DBSession
        )

        ret_question_types = utils._decode_question_types(question_types)

    except:
        raise Exception("Database error.")

    return ret_question_types

def get_assignments(start, count):

    ret_assignments = []
    
    try:

        assignments = Assignments.get_all_with_questions(
            session = DBSession,
            token = None,
            start = start,
            count = count,
        )

        ret_assignments = utils._decode_assignments(assignments)

    except:
        raise Exception("Database error.")

    return ret_assignments

def get_posts(start, count, deleted):

    ret_posts = []
    
    try:

        posts = Posts.get_posts(
            DBSession,
            deleted = deleted,
            start = start,
            count = count,
        )

        ret_posts = utils._decode_posts(posts)

    except:
        raise Exception("Database error.")

    return ret_posts

def get_post(post_id):#, start, count):

    ret_posts = []

    try:

        posts = Posts.get_with_media_objects_from_post_id(
            session = DBSession,
            post_id = post_id,
            #start = start,
            #count = count,
        )

        ret_posts = utils._decode_posts(posts)

    except:
        raise Exception("Database error.")

    return ret_posts

def delete_post(post_id):

    post = None
    
    try:

        post = Posts.delete_post(
            session = DBSession,
            post_id = post_id,
        )

    except:
        raise Exception("Database error.")

    return post

def approve_post(post_id):

    post = None
    
    try:

        post = Posts.approve_post(
            session = DBSession,
            post_id = post_id,
        )

    except:
        raise Exception("Database error.")

    return post

def register_post_view(organization_id, post_id):

    post = None
    client = None
    notification = None
    
    try:

        post = Posts.get_from_post_id(
            session = DBSession,
            post_id = post_id,
        )

        client = Clients.increment_view_count(
            session = DBSession,
            client_id = post.client_id,
        )

        organization = Organizations.get_from_id(
            session = DBSession,
            organization_id = organization_id,
        )

        notification = Notifications.create_notification(
            session = DBSession,
            client_id = post.client_id,
            notification_type = 'post_viewed',
            payload = json.dumps({
                'organization': organization.name,
            })
        )

    except:
        raise Exception("Database error.")

    return post, client, notification

def get_response_posts(assignment_id, start, count, deleted):

    ret_posts = []
    
    try:

        posts = Posts.get_all_from_assignment_id(
            session = DBSession,
            assignment_id = assignment_id,
            deleted = deleted,
            start = start,
            count = count,
        )

        ret_posts = utils._decode_posts(posts)

    except:
        raise Exception("Database error.")

    return ret_posts

def get_collection_posts(collection_id, start, count):

    ret_posts = []

    try:

        posts = Posts.get_all_from_collection_id(
            session = DBSession,
            collection_id = collection_id,
            start = start,
            count = count,
        )

        ret_posts = utils._decode_posts(posts)

    except:
        raise Exception("Database error.")

    return ret_posts

def get_client_posts(cuid, start, count):

    ret_posts = []
    
    try:

        posts = Posts.get_all_from_cuid(
            session = DBSession,
            cuid = cuid,
            start = start,
            count = count,
        )

        ret_posts = utils._decode_posts(posts)

    except:
        raise Exception("Database error.")

    return ret_posts

def get_collections(user_id):
    
    ret_collections = []

    try:

        collections = Collections.get_all_from_user_id(
           session = DBSession,
           user_id = user_id,
        )

        ret_collections = utils._decode_collections(collections)

    except:
        raise Exception("Database error.")

    return ret_collections

def create_collection(user_id, name, description, tags):

    collection = None

    try:

        collection = Collections.add_collection( #_from_http(
            session = DBSession,
            user_id = user_id,
            name = name,
            description = description,
            tags = tags,
        )

    except:
        raise Exception("Database error.")

    return collection

def add_post_to_collection(collection_id, post_id):

    collection_post = None
    
    try:

        _collection = Collections.get_from_collection_id(
            session = DBSession,
            collection_id = collection_id,
        )

        _post = Posts.get_from_post_id(
            session = DBSession,
            post_id = post_id,
        )

        collection_post = None
        if _collection is not None and _post is not None:
            collection_post = Collections.add_post_to_collection(
                session = DBSession,
                collection_id = collection_id,
                post_id = post_id,
            )

    except:
        raise Exception("Database error.")

    return collection_post

def get_organizations():

    ret_organizations = []

    try:

        organizations = Organizations.get_all(
            session = DBSession,
        )

        ret_organizations = utils._decode_organizations(organizations)

    except:
        raise Exception("Database error.")

    return ret_organizations

def create_organization(user_type_id, name, description, contact_name, \
        contact_email):

    organization = None

    try:

        if check_super_user(user_type_id):

            organization = Organizations.add_organization( #_from_http(
                session = DBSession,
                name = name,
                description = description,
                contact_name = contact_name,
                contact_email = contact_email,
            )

    except:
        raise Exception("Database error.")

    return organization

def create_question(user_id, language_code, question_text, description, \
        question_type, answers):

    question = None

    try:

        # back fill with empty strings
        for i in range(len(answers),10):
            answers.append('')

        question = Questions.add_question(
            session = DBSession,
            user_id = user_id,
            language_code = language_code,
            question_text = question_text,
            description = description,
            question_type = question_type,
            answers = answers,
        )

    except:
        raise Exception("Database error.")

    return question

def create_assignment(user_id, name, life_time, top_left_lat, top_left_lng, \
        bottom_right_lat, bottom_right_lng, questions):

    assignment = None
    collection = None
    
    try:

        # create assignment
        assignment = Assignments.create_from_http(
            session = DBSession,
            user_id = user_id,
            name = name,
            life_time = life_time,
            #geo_fence = geo_fence,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
        )

        collection = Collections.add_collection( #_from_http(
            session = DBSession,
            user_id = user_id,
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

    except:
        raise Exception("Database error.")

    return assignment, collection

def create_story(user_id, title, tags, contents, top_left_lat, top_left_lng, \
         bottom_right_lat, bottom_right_lng, language_code):

    story = None
    
    try:

        story = Stories.add_story(
            session = DBSession,
            #token = user.token,
            user_id = user_id,
            title = title,
            tags = tags,
            #top_text = top_text,
            #media_id = banner_media_id,
            contents = contents,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
            #use_fence = use_fense,
            language_code = language_code,
        )

    except:
        raise Exception("Database error.")

    return story
