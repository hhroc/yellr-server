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

def ago_decode(dt):

    SECOND = 1
    MINUTE = SECOND * 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    ago = 0
    diff = (datetime.datetime.now() - dt).total_seconds();
    if diff > DAY:
       ago = "%id" % int(float(diff / DAY))
    elif diff > HOUR:
       ago = "%ih" % int(float(diff / HOUR))
    elif diff > MINUTE:
       ago = "%im" % int(float(diff / MINUTE))
    else:
       ago = "1m"

    return ago

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

    ret_languages = []

    try:
        
        for language_code, name in languages:
            ret_languages.append({
                'name': name,
                'code': language_code,
            })

    except:
        raise Exception("Database error.")

    return ret_languages


def _decode_question_types(question_types):

    ret_question_types = []
    
    try:
    
        for question_type_id, question_type_text, question_type_description \
                in question_types:
            ret_question_types.append({
                'question_type_id': question_type_id,
                'question_type_text': question_type_text,
                'question_type_description': question_type_description,
            })
            
    except:
        raise Exception("Database error.")


    return ret_question_types

def _decode_assignments(assignments):

    ret_assignments = []

    try:

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
                    language_code, post_count, response_count in assignments:

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
                        'language_code': language_code,
                        'post_count': post_count,
                        'response_count': response_count,
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

    except:
        raise Exception("Database error.")

    return ret_assignments

def _decode_posts(posts, clean=False):

    ret_posts = []

    try:

        if len(posts) > 0 and posts[0][0] != None:

            seen_post_ids = []
            post = {}

            # itterate throught the list, and build our resposne
            index = 0
            for post_id, client_id, post_datetime, deleted, \
                    lat, lng, approved, flagged, media_object_id, media_id, \
                    file_name, caption, media_text, media_type_name, \
                    media_type_description, verified, first_name, last_name, \
                    cuid, language_code, language_name, assignment_id, \
                    assignment_name, question_text, up_vote_count, \
                    down_vote_count, has_voted, is_up_vote in posts:

                if (post_id not in seen_post_ids) or (index == len(posts)-1):

                    if post:
                        ret_posts.append(post)

                    # build the response that is clean (can be sent to the client)
                    post = {
                        # need to include post id to support voting.
                        # todo: obfuscate this some how ...
                        'post_id': post_id,
                        'post_datetime': str(post_datetime),
                        'post_datetime_ago': ago_decode(post_datetime),
                        'verified_user': bool(verified),
                        'first_name': first_name,
                        'last_name': last_name,
                        'language_code': language_code,
                        'language_name': language_name,
                        'question_text': question_text,
                        'up_vote_count': up_vote_count,
                        'down_vote_count': down_vote_count,
                        'has_voted': has_voted,
                        'is_up_vote': is_up_vote,
                        'media_objects': []
                    }

                    # add the additional fields if it is a unclean (from the
                    # moderator site) request.
                    if clean == False:
                        post['deleted'] = deleted
                        post['lat'] = lat
                        post['lng'] = lng
                        post['approved'] = approved
                        post['flagged'] = flagged
                        post['verified_user'] = bool(verified)
                        post['client_id'] = client_id
                        post['assignment_id'] = assignment_id
                        post['assignment_name'] = assignment_name

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

    except:
        raise Exception("Database error.")

    return ret_posts

def _decode_collections(collections):

    ret_collections = []

    try:

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

    except:
        raise Exception("Database error.")

    return ret_collections

def _decode_organizations(organizations):

    ret_organizations = []

    try:

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

    except:
        raise Exception("Database error.")

    return ret_organizations

