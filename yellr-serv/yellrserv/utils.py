import json
import datetime
import os

import markdown

from pyramid.response import Response

from .models import (
    DBSession,
    #UserTypes,
    #Users,
    #Clients,
    Assignments,
    #Questions,
    #QuestionAssignments,
    #Languages,
    #Posts,
    #MediaTypes,
    #MediaObjects,
    #PostMediaObjects,
    Stories,
    #ClientLogs,
    #Collections,
    #CollectionPosts,
    Messages,
    Notifications,
    )


def make_response(resp_dict, status_code=200):

    print "[DEBUG]"
    print resp_dict
    print '\n'

    resp = Response(json.dumps(resp_dict), content_type='application/json') #, charset='utf8')
    resp.headerlist.append(('Access-Control-Allow-Origin', '*'))

    resp.status = status_code

    return resp

#def admin_log(log_text):
#
#    with open('log.txt', 'a') as f:
#        f.write('[{0}] {1}\n'.format(str(datetime.datetime.now()),log_text))

def _decode_languages(languages):

    if True:

        ret_languages = []
        
        for language_code, name in languages:
            ret_languages.append({
                'name': name,
                'code': language_code,
            })

    return ret_languages


def _decode_question_types(question_types):

    if True:

        ret_question_types = []
    
        for question_type_id, question_type_text, question_type_description \
                in question_types:
            ret_question_types.append({
                'question_type_id': question_type_id,
                'question_type_text': question_type_text,
                'question_type_description': question_type_description,
            })

    return ret_question_types

def _decode_assignments(assignments):

    if True:

        ret_assignments = []

        if len(assignments) > 0 and assignments[0][0] != None:

            seen_assignment_ids = []
            assignment = {}

            # itterate throught he list, and build our resposne
            index = 0
            for assignment_id, publish_datetime, expire_datetime, name, \
                    top_left_lat, top_left_lng, bottom_right_lat, \
                    bottom_right_lng, use_fence, collection_id, org_id, \
                    org_name, org_description, question_text, \
                    question_type_id, question_description, \
                    answer0, answer1, answer2, answer3, answer4, answer5, \
                    answer6, answer7, answer8, answer9, language_id, \
                    language_code, post_count in assignments:

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
                        'organization_id': org_id,
                        'organization': org_name,
                        'organization_description': org_description,
                        'questions': [],
                        'post_count': post_count,
                        'language_code': language_code,
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

    return ret_assignments

def _decode_posts(posts):

    if True:

        ret_posts = []

        if len(posts) > 0 and posts[0][0] != None:

            seen_post_ids = []
            post = {}

            # itterate throught the list, and build our resposne
            index = 0
            for post_id, client_id, post_datetime, deleted, \
                    lat, lng, approved, media_object_id, media_id, \
                    file_name, caption, media_text, media_type_name, \
                    media_type_description, verified, cuid, \
                    language_code, language_name, assignment_id, \
                    assignment_name in posts:

                if (post_id not in seen_post_ids) or (index == len(posts)-1):

                    if post:

                        ret_posts.append(post)

                    post = {
                        'post_id': post_id,
                        'client_id': client_id,
                        #'title': title,
                        'post_datetime': str(post_datetime),
                        'deleted': deleted,
                        'lat': lat,
                        'lng': lng,
                        'approved': approved,
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

    return ret_posts

def _decode_collections(collections):

    if True:

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

    return ret_collections

def _decode_organizations(organizations):

    if True:

        ret_organizations = []

        for org_id, name, desc, contact_name, contact_email, created \
                in organizations:

            ret_organizations.append({
                'id': org_id,
                'name': name,
                'description': desc,
                'contact_name': contact_name,
                'contact_email': contact_email,
                'created': str(created),
            })

    return ret_organizations

