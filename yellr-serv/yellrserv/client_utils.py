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

def get_assignments(language_code, lat, lng):

    assignments = Assignments.get_all_open_with_questions(
        session = DBSession,
        language_code = language_code,
        lat = lat,
        lng = lng
    )
    
    ret_assignments = []
    for assignment_id, publish_datetime, expire_datetime, name, \
            top_left_lat, top_left_lng, bottom_right_lat, \
            bottom_right_lng, use_fence, collection_id, organization,\
            question_text, question_type_id, description, answer0, \
            answer1, answer2, answer3, answer4, answer5, answer6, \
            answer7, answer8, answer9, post_count in assignments:
        ret_assignments.append({
            'assignment_id': assignment_id,
            'organization': organization,
            'publish_datetime': str(publish_datetime),
            'expire_datetime': str(expire_datetime),
            'name': name,
            'top_left_lat': top_left_lat,
            'top_left_lng': top_left_lng,
            'bottom_right_lat': bottom_right_lat,
            'bottom_right_lng': bottom_right_lng,
            'question_text': question_text,
            'question_type_id': question_type_id,
            'description': description,
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
            'post_count': post_count,
        })

    return ret_assignments

def get_stories(language_code, lat, lng):

    stories, total_story_count = Stories.get_stories(
        session = DBSession,
        lat = lat,
        lng = lng,
        language_code = language_code,
        start = 0, #start,
        count = 15, #count,
    )

    ret_stories = []
    for story_unique_id, publish_datetime, edited_datetime, title, tags, \
            top_text, contents, top_left_lat, top_left_lng, \
            bottom_right_lat, bottom_right_lng, first_name, last_name, \
            organization, email, media_file_name, media_id in stories:
        ret_stories.append({
            'story_unique_id': story_unique_id,
            'publish_datetime': str(publish_datetime),
            'edited_datetime': str(edited_datetime),
            'title': title,
            'tags': tags,
            'top_text': top_text,
            #'contents': contents,
            'contents_rendered': markdown.markdown(contents),
            'top_left_lat': top_left_lat,
            'top_left_lng': top_left_lng,
            'bottom_right_lat': bottom_right_lat,
            'bottom_right_lng': bottom_right_lng,
            'author_first_name': first_name,
            'author_last_name': last_name,
            'author_organization': organization,
            'author_email': email,
            'banner_media_file_name': media_file_name,
            'banner_media_id': media_id,
        })

    return ret_stories

def get_notifications(client_id, language_code, lat, lng):

    notifications = Notifications.get_notifications_from_client_id(
        session = DBSession,
        client_id = client_id, #client.client_id,
    )

    ret_notifications = []
    for notification_id, notification_datetime, \
            notification_type, payload in notifications:
        ret_notifications.append({
            'notification_id': notification_id,
            'notification_datetime': str(notification_datetime),
            'notification_type': notification_type,
            'payload': json.loads(payload),
        })

    return ret_notifications

def get_messages(client_id, language_code, lat, lng):

    messages = Messages.get_messages_from_client_id(
        session = DBSession,
        client_id = client_id, #client.client_id
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

    return ret_messages

    
