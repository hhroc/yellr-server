import os
import json
from time import strftime
import uuid
import datetime
import subprocess
import magic
import mutagen.mp3
import mutagen.oggvorbis
import mutagen.mp4

#from utils import utils.make_response
import utils
import client_utils

import urllib

import markdown
import transaction

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError


from .models import (
    DBSession,
    UserTypes,
    #Users,
    Clients,
    Assignments,
    Questions,
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
    Zipcodes,
    )

from config import system_config

SERVER_VERSION = '0.0.1'
REQUIRED_CLIENT_VERSION = '0.0.1'

system_status = {
    'alive': True,
    'launchtime': str(strftime("%Y-%m-%d %H:%M:%S")),
}

@view_config(route_name='index', renderer='templates/index.mak')
def index(request):

    ret_latest_stories = []

    try:
    #if True:

        latest_stories,dummy = Stories.get_stories(
            session = DBSession,
            lat = 43.1,
            lng = -77.5,
            language_code = 'en',
        )

        #ret_latest_stories = []
        for story_unique_id, publish_datetime, edited_datetime, title, tags, \
                top_text, contents, top_left_lat, top_left_lng, \
                bottom_right_lat, bottom_right_lng, first_name, last_name, \
                organization, email, media_file_name, media_id in latest_stories:

            preview_text = ' '.join(contents.split(' ')[:30])

            ret_latest_stories.append({
                'story_unique_id': story_unique_id,
                'publish_datetime': str(publish_datetime),
                'edited_datetime': str(edited_datetime),
                'title': title,
                'tags': tags,
                'top_text': top_text,
                'contents': markdown.markdown(contents),
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
                'preview_text': preview_text,
            })

    except:
        pass

    # print ret_stories
    return {'title': 'Yellr - Frontpage', 'data_page': 'index','stories': True, 'latest_stories': ret_latest_stories}



@view_config(route_name='submit-tip.html', renderer='templates/submit-tip.mak')
def submit_tip(request):
    return dict(title='Submit Tip', data_page='submit-tip')

def register_client(request):

    success = False
    error_text = ''
    language_code = ''
    lat = 0
    lng = 0
    client = None
    try:
    #if True:
        cuid = request.GET['cuid']
        language_code = request.GET['language_code']
        lat = float(request.GET['lat'])
        lng = float(request.GET['lng'])

        print request.GET
        print request.POST

        # creates client if not yet seen
        client = Clients.get_client_by_cuid(
            session = DBSession,
            cuid = cuid,
            lat = lat,
            lng = lng,
        )

        Clients.check_in(
            session = DBSession,
            cuid = cuid,
            lat = lat,
            lng = lng,
        )

        success = True
    except:
        error_text = "Required Fields: cuid, language_code, lat, lng"

    return success, error_text, language_code, lat, lng, client

@view_config(route_name="zipcode_lookup.json")
def zipcode_loopup(request):
    
    result = {'success': False }
    status_code = 200
    #if True:
    try:

        success, error_text, language_code, lat, lng, client = \
            register_client(request)
        if success == False:
            raise Exception(error_text)

        try:
            _zipcode = request.GET['zipcode']
        except:
            result['error_text'] = "Missing Field: zipcode"
            raise Exception('Missing Field: zipcode')

        zipcode = Zipcodes.get_from_zipcode(
            session = DBSession,
            _zipcode = _zipcode,
        )

        if zipcode != None:
            result['zipcode'] = zipcode.zipcode
            result['city'] = zipcode.city
	    result['state_code'] = zipcode.state_code
            result['lat'] = zipcode.lat
            result['lng'] = zipcode.lng  
            result['success'] = True

    except:
        status_code = 400
        pass

    return utils.make_response(result, status_code)

@view_config(route_name="get_data.json")
def get_data(request):

    result = {'success': False}
    try:
    #if True:
        success, error_text, language_code, lat, lng, client = \
            register_client(request)
        if success == False:
            raise Exception(error_text)

        assignments = utils.get_assignments(language_code, lat, lng)
        stories = utils.get_stories(language_code, lat, lng)
        notifications = utils.get_notifications(client.client_id, language_code, lat, lng)
        messages = utils.get_messages(client.client_id, language_code, lat, lng)

        result['assignments'] = assignments
        result['stories'] = stories
        result['notifications'] = [] #notifications
        result['messages'] = [] #messages

        result['success'] = True

    except:
        pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'get_data.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result)

@view_config(route_name='get_assignments.json')
def get_assignments(request):

    result = {'success': False}

    #try:
    if True:
        success, error_text, language_code, lat, lng, client = \
            register_client(request)
        if success == False:
            raise Exception(error_text)

        assignments = Assignments.get_all_open_with_questions(
            session = DBSession,
            language_code = language_code,
            lat = lat,
            lng = lng
        )

        ret_assignments = []
        for assignment_id, publish_datetime, expire_datetime, name, \
                top_left_lat, top_left_lng, bottom_right_lat, \
                bottom_right_lng, use_fence, collection_id, org_id, \
                org_name, org_description, question_text, \
                question_type_id, description, answer0, \
                answer1, answer2, answer3, answer4, answer5, answer6, \
                answer7, answer8, answer9, language_id, language_code, \
                post_count in assignments:
            ret_assignments.append({
                'assignment_id': assignment_id,
                #'organization_id': org_id,
                'organization': org_name,
                'organization_descriotion': org_description,
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
                'language_code': language_code,
            })
                    
        result['assignments'] = ret_assignments
        result['success'] = True

    #except:
    #    pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'get_assignments.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result)

@view_config(route_name='get_notifications.json')
def get_notifications(request):

    result = {'success': False}

    try:
    #if True:
        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)

        notifications = Notifications.get_notifications_from_client_id(
            session = DBSession,
            client_id = client.client_id,
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

        result['notifications'] = ret_notifications
        result['success'] = True

    except Exception, e:
        pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'get_notifications.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result)

@view_config(route_name='create_response_message.json')
def create_response_message(request):

    result = {'success': False}

    try:

        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)

        message = Messages.create_response_message_from_http(
            session = DBSession,
            client_id = client_id,
            parent_message_id = parent_message_id,
            subject = subject,
            text = text,
        )

        if message != None:
            result['message_id'] = message.message_id
            result['success'] = True
        else:
            result['error_text'] = "Message already has posted response."

    except:
        pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'create_response_message.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result)

@view_config(route_name='get_messages.json')
def get_messages(request):

    result = {'success': False}

    try:

        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)

        messages = Messages.get_messages_from_client_id(
            session = DBSession,
            client_id = client.client_id
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

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'get_messages.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )
 
    return utils.make_response(result)

@view_config(route_name='get_stories.json')
def get_stories(request):

    result = {'success': False}

    #try:
    if True:
        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)
 
        start = 0
        count = 25
        try:
            if 'start' in reqeusts.GET:
                start = int(float(request.GET['start']))
            if 'count' in request.GET:
                count = int(float(request.GET['count']))
        except:
            pass

        stories, total_story_count = Stories.get_stories(
            session = DBSession,
            lat = lat,
            lng = lng,
            language_code = language_code,
            start = start,
            count = count,
        )

        ret_stories = []
        for story_unique_id, publish_datetime, edited_datetime, title, tags, \
                contents, top_left_lat, top_left_lng, bottom_right_lat, \
                bottom_right_lng, first_name, last_name, organization_id, \
                organization_name, email in stories:
            ret_stories.append({
                'story_unique_id': story_unique_id,
                'publish_datetime': str(publish_datetime),
                'edited_datetime': str(edited_datetime),
                'title': title,
                'tags': tags,
                #'top_text': top_text,
                #'contents': contents,
                'contents_rendered': markdown.markdown(contents),
                'top_left_lat': top_left_lat,
                'top_left_lng': top_left_lng,
                'bottom_right_lat': bottom_right_lat,
                'bottom_right_lng': bottom_right_lng,
                'author_first_name': first_name,
                'author_last_name': last_name,
                'author_organization': organization_name,
                'author_email': email,
                #'banner_media_file_name': media_file_name,
                #'banner_media_id': media_id,
            })

        result['total_story_count'] = total_story_count
        result['stories'] = ret_stories
        result['success'] = True

    #except:
    #    pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'get_stories.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result)


@view_config(route_name='publish_post.json')
def publish_post(request):

    """
    HTTP POST with the following fields:

    client_id, type: text (unique client id)
    assignment_id, type: text ( '' for no assignment)
    language_code, type: text (two letter language code)
    lat, type: text (latitude in degrees)
    lng, type: text (longitude in degrees)
    media_objects, type: text (json array of media id's)

    """

    result = {'success': False}
    status_code = 200

    try:
    #if True:
        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)

        assignment_id = 0
        try:
            if 'assignment_id' in request.POST:
                assignment_id = int(float(str(request.POST['assignment_id'])))
        except:
            pass

        media_obects = []
        try:
             media_objects = json.loads(urllib.unquote(
                request.POST['media_objects']).decode('utf8')
            )
        except:
            raise Exception("Missing or invalid MediaObjects JSON list")

        post = Posts.create_from_http(
            session = DBSession,
            client_id = client.client_id,
            assignment_id = assignment_id,
            #title = '', #title,
            language_code = language_code,
            lat = lat,
            lng = lng,
            media_objects = media_objects, # array
        )

        result['success'] = True
        result['post_id'] = post.post_id
        #result['new_user'] = created

    except:
       status_code = 400

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'publish_post.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result, status_code)

@view_config(route_name='upload_media.json')
def upload_media(request):

    """
    HTTP POST with the following fields:

    media_file, type: file
    client_id, type: text
    media_type, type: text
        where valid mediatypes are: 'text', 'audio', 'video', 'image'

    optional fields:

    media_text, type: text
    media_caption, type: text

    """

    result = {'success': False}
    status_code = 200

    #try:
    if True:
        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)
 
        try:
            media_type = request.POST['media_type']
        except:
            error_text = "Missing media type field"
            raise Exception(error_text)

        ret_file_name = ''
        preview_file_name = ''
        file_path = ''
        if media_type == 'image' or media_type == 'video' \
                or media_type == 'audio':

            #if True:
            try:
                media_file_name = request.POST['media_file'].filename
                input_file = request.POST['media_file'].file
            except:
                result['error_text'] = 'Missing or invalid file field'
                raise Exception('Invalid media_file field.')

            #media_extention="processing"

            # generate a unique file name to store the file to
            unique = str(uuid.uuid4())
            #file_name = '{0}'.format(unique) #,media_extention)
            temp_file_name = os.path.join(system_config['upload_dir'], unique)

            # write file to temp location, and then to disk
            temp_file_path = temp_file_name + '~'
            output_file = open(temp_file_path, 'wb')

            # Finally write the data to disk
            input_file.seek(0)
            while True:
                data = input_file.read(2<<16)
                if not data:
                    break
                output_file.write(data)

            output_file.close()

            #decode media type of written file
            if media_type == 'image':

                # type incoming file
                mime_type = magic.from_file(temp_file_path, mime=True)
                allowed_image_types = [
                    'image/jpeg',
                    'image/png',
                    'image/x-ms-bmp',
                    'image/tiff',
                ]

                #if not mime_type in allowed_image_types:     
                #    raise Exception("Unsupported Image Type: %s" % mime_type)

                # convert to jpeg from whatever format it was
                try:
                    
                    subprocess.call(['convert', temp_file_path, '{0}.jpg'.format(temp_file_name)])
                    image_file_path = '{0}.jpg'.format(temp_file_name)

                    os.remove(temp_file_path)
                    ret_file_name = image_file_path

                except Exception, ex:
                    error_text = "Error converting image: {0}".format(ex)
                    raise Exception(error_text)

                #strip metadata from images with ImageMagick's mogrify
                try:

                    # strip meta data
                    subprocess.call(['mogrify', '-strip', image_file_path])
                    
                except Exception, ex:
                    error_text = "Error removing metadata: {0}".format(ex)
                    raise Exception(error_text)

                # create preview image 
                try:

                    preview_file_name = '{0}p.jpg'.format(unique)
                    file_path_image_preview = os.path.join(system_config['upload_dir'], preview_file_name)

                    subprocess.call(['convert', image_file_path, '-resize', '450', '-size', '450', \
                        file_path_image_preview])

                except Exception, ex:
                    error_text = "Error generating preview image: {0}".format(ex)
                    raise Exception(error_text)

                file_path = "{0}.jpg".format(file_path)

            
            #process video files
            elif media_type == 'video':
                '''
                #I can't seem to find any evidence of PII in mpg metadata
                if mimetype == "video/mpeg":
                    media_extention = 'mpg'
                elif mimetype == "video/mp4":
                    media_extension = "mp4"
                    #strip metadata
                    try:
                        mp4 = mutagen.mp4.MP4(temp_file_path)
                        mp4.delete()
                        mp4.save()
                    except:
                        error_text = "Something went wrong while stripping metadata from mp4"
                        raise Exception('')

                else:
                    error_text = 'invalid video file'
                    raise Exception('')
                '''
                pass

            #process audio files
            elif media_type == 'audio':
                '''
                #mp3 file
                if mimetype == "audio/mpeg":
                    media_extention = 'mp3'
                    #strip metadata
                    try:
                        mp3 = mutagen.mp3.MP3(temp_file_path)
                        mp3.delete()
                        mp3.save()
                    except:
                        error_text = "Something went wrong while stripping metadata from mp3"
                        raise Exception('')

                #ogg vorbis file
                elif mimetype == "audio/ogg" or mimetype == "application/ogg":
                    media_extention = 'ogg'
                    try:
                        ogg = mutagen.oggvorbis.Open(temp_file_path)
                        ogg.delete()
                        ogg.save()
                    except:
                        error_text = "Something went wrong while stripping metadata from ogg vorbis"
                        raise Exception('')

                #not mp3 or ogg vorbis
                else:
                    error_text = 'invalid audio file'
                    raise Exception('')
                '''
                pass

            #I don't think the user has a way to upload files of this type besides typing in the box
            #so it doesn't need as robust detection.
            elif media_type == 'text':
                #media_extention = 'txt'
                pass
            else:
                error_text = 'invalid media type'
                raise Exception('')

            #the file has been validated and processed, so we adjust the file path
            #to the mimetype-dictated file extension
            #file_path = file_path.replace("processing", media_extention)

            # rename once we are valid
            #os.rename(temp_file_path, file_path)
            #os.remove(temp_file_path)

            #result['file_name'] = os.path.basename(file_path)
            #result['preview_file_name'] = os.path.basename(preview_file_name)

        #except:
            #result['error_text'] = 'Missing or invalid media_file contents.'
            #raise Exception('missing/invalid media_file contents')

        caption = ''
        #if True:
        try:
            caption = request.POST['caption']
        except:
            try:
                caption = request.POST['media_caption']
            except:
                pass

        media_text = ''
        if media_type == 'text':
            try:
                media_text = request.POST['media_text']
            except:
                raise Exception('Invalid/missing field')

        # register file with database, and get file id back
        media_object = MediaObjects.create_new_media_object(
            session = DBSession,
            client_id = client.client_id,
            media_type_text = media_type,
            file_name = os.path.basename(ret_file_name), #os.path.basename(file_path),
            caption = caption,
            media_text = media_text,
        )

        result['media_id'] = media_object.media_id
        result['success'] = True
        #result['new_user'] = created
        #result['media_text'] = media_text
        #result['error_text'] = ''

    #except:
    #    status_code = 400
    #    pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'upload_media.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result, status_code)

@view_config(route_name='get_profile.json')
def get_profile(request):

    result = {'success': False}
    
    try:
    #if True:

        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)
 
        #user,created = Users.get_from_client_id(
        #    session = DBSession,
        #    client_id = client.client_id,
        #)

        #client = Clients.get_client_by_cuid(
        #    session = DBSession,
        #    cuid = cuid,
        #)

        

        post_count = Posts.get_count_from_client_id(
            session = DBSession,
            client_id = client.client_id,
        )

        result['client_id'] = client.client_id
        result['first_name'] = client.first_name
        result['last_name'] = client.last_name
        result['organization'] = '' #client.organization
        result['email'] = client.email
        result['verified']  = client.verified

        result['post_count'] = post_count
        result['post_view_count'] = client.post_view_count
        result['post_used_count'] = client.post_used_count

        result['success'] = True

    except:
        pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'get_profile.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result)

@view_config(route_name='verify_client.json')
def verify_user(request):

    result = {'success': False}

    try:

        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)

        

        #exists = Users.check_exists(
        #    session = DBSession,
        #    user_name = user_name,
        #    email = email,
        #    client_id = client_id,
        #)
        
        #if exists == True:
        #    result['error_text'] = "Username, email, and/or client ID already registered"
        #    raise Exception("username, email, and/or client ID already registered")
        #else:
        #    verified_new_user = Users.verify_user(
        #        session = DBSession,
        #        client_id = client_id,
        #        user_name = user_name,
        #        password = password,
        #        first_name = first_name,
        #        last_name = last_name,
        #        email = email,
        #    )
        #    result['verfied_user_id'] = verified_new_user.user_id
        #    
        #    result['success'] = True

    except:
        pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'verify_user.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result)
@view_config(route_name='get_approved_posts.json')
def get_approved_posts(request):

    result = {'success': False}

    #try:
    if True:

        success, error_text, language_code, lat, lng, \
            client = register_client(request)
        if success == False:
            raise Exception(error_text)

        start = 0
        count = 50
        try:
            if 'start' in reqeusts.GET:
                start = int(float(request.GET['start']))
            if 'count' in request.GET:
                count = int(float(request.GET['count']))
        except:
            pass

        #user,created = Users.get_from_client_id(
        #    session = DBSession,
        #    client_id = client.client_id,
        #)

        #client = Clients.get_client_by_cuid(
        #    session = DBSession,
        #    cuid = cuid,
        #)

        posts = client_utils.get_approved_posts(
            client_id = client.client_id,
            language_code = language_code,
            lat = lat,
            lng = lng,
            start = start,
            count = count,
        )

        result['posts'] = posts

        #post_count = Posts.get_count_from_client_id(
        #    session = DBSession,
        #    client_id = client.client_id,
        #)

        #result['client_id'] = client.client_id
        #result['first_name'] = client.first_name
        #result['last_name'] = client.last_name
        #result['organization'] = '' #client.organization
        #result['email'] = client.email
        #result['verified']  = client.verified

        #result['post_count'] = post_count
        #result['post_view_count'] = client.post_view_count
        #result['post_used_count'] = client.post_used_count

        result['success'] = True

    #except:
    #    pass

    client_id = None
    if client != None:
        client_id = client.client_id
    ClientLogs.log(
        session = DBSession,
        client_id = client_id,
        url = 'get_approved_posts.json',
        lat = lat,
        lng = lng,
        request = json.dumps({
            'get': '{0}'.format(request.GET),
            'post': '{0}'.format(request.POST),
        }),
        result = json.dumps(result),
        success = success,
    )

    return utils.make_response(result)

