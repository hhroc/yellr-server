import json
import datetime

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

def admin_log(log_text):

    with open('log.txt', 'a') as f:
        f.write('[{0}] {1}\n'.format(str(datetime.datetime.now()),log_text))

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
                    bottom_right_lng, use_fence, collection_id, organization, \
                    question_text, question_type_id, question_description, \
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
                        'organization': organization,
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

