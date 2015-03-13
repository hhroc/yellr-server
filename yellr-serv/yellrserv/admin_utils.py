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
    #Clients,
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

    print "\n\nREQUEST.GET:"
    print request.GET
    print "\n\nREQUEST.POST:"
    print request.POST
    print "\n\nREQUEST.SESSION:"
    print request.session

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

def authenticate(username, password):

    if True:

        user = None
        token = None
        fence = None

        user, org, token = Users.authenticate(DBSession, username, password)

        if token == None:
            result['error_text'] = 'Invalid credentials'
            #raise Exception('invalid credentials')
        else:

            fence = UserGeoFences.get_fence_from_user_id(
                session = DBSession,
                user_id = user.user_id,
            )

    return user, org, token, fence

def check_super_user(user_type_id):

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

    return is_super_user

def create_user(user_type_id, user_type_name, user_name, password, first_name,\
         last_name, email, organization_id, top_left_lat, top_left_lng,\
         bottom_right_lat, bottom_right_lng):

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

    return new_user

def get_languages():

    languages = Languages.get_all(
        session = DBSession
    )

    return utils._decode_languages(languages)

def get_question_types():

    question_types = QuestionTypes.get_all(
        session = DBSession
    )

    return utils._decode_question_types(question_types)

def get_assignments(start, count):

    assignments = Assignments.get_all_with_questions(
        session = DBSession,
        token = None,
        start = start,
        count = count,
    )

    return utils._decode_assignments(assignments)

def get_posts(start, count, deleted):

    posts = Posts.get_posts(
        DBSession,
        deleted = deleted,
        start = start,
        count = count,
    )

    return utils._decode_posts(posts)

def get_post(post_id):#, start, count):

    posts = Posts.get_with_media_objects_from_post_id(
        session = DBSession,
        post_id = post_id,
        #start = start,
        #count = count,
    )

    return utils._decode_posts(posts)

def delete_post(post_id):

    post = Posts.delete_post(
        session = DBSession,
        post_id = post_id,
    )

    return post

def get_response_posts(assignment_id, start, count, deleted):

    posts = Posts.get_all_from_assignment_id(
        session = DBSession,
        assignment_id = assignment_id,
        deleted = deleted,
        start = start,
        count = count,
    )

    return utils._decode_posts(posts)

def get_collection_posts(collection_id, start, count):

    posts = Posts.get_all_from_collection_id(
        session = DBSession,
        collection_id = collection_id,
        start = start,
        count = count,
    )

    return utils._decode_posts(posts)

def get_client_posts(cuid, start, count):

    posts = Posts.get_all_from_cuid(
        session = DBSession,
        cuid = cuid,
        start = start,
        count = count,
    )

    return utils._decode_posts(posts)

def get_collections(user_id):

    collections = Collections.get_all_from_user_id(
       session = DBSession,
       user_id = user_id,
    )

    return utils._decode_collections(collections)

def create_collection(user_id, name, description, tags):

    collection = Collections.add_collection( #_from_http(
        session = DBSession,
        user_id = user_id,
        name = name,
        description = description,
        tags = tags,
    )

    return collection

def add_post_to_collection(collection_id, post_id):

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

    return collection_post

def get_organizations():

    organizations = Organizations.get_all(
        session = DBSession,
    )

    return utils._decode_organizations(organizations)

def create_organization(user_type_id, name, description, contact_name, \
        contact_email):

    organization = None
    if check_super_user(user_type_id):

        organization = Organizations.add_organization( #_from_http(
            session = DBSession,
            name = name,
            description = description,
            contact_name = contact_name,
            contact_email = contact_email,
        )

    return organization

def create_question(user_id, language_code, question_text, description, \
        question_type, answers):

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

    return question

def create_assignment(user_id, name, life_time, top_left_lat, top_left_lng, \
        bottom_right_lat, bottom_right_lng, questions):

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

    return assignment, collection

def create_story(user_id, title, tags, contents, top_left_lat, top_left_lng, \
         bottom_right_lat, bottom_right_lng, language_code):

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

    return story
