import os
import json
import urllib
import uuid

#import subprocess
#import magic
#import mutagen.mp3
#import mutagen.oggvorbis
#import mutagen.mp4

from pyramid.view import view_config

import client_utils
import utils
from config import system_config

@view_config(route_name='get_local_posts.json')
def get_local_posts(request):

    result = {'success': False}
    status_code = 200

    #try:
    if True:
        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        try:
            start = 0
            if 'start' in request.GET:
                start = int(float(request.GET['start']))
            count = 75
            if 'count' in request.GET:
                count = int(float(request.GET['count']))
        except:
            status_code = 403
            raise Exception("Invalid input.")

        posts = client_utils.get_approved_posts(
            client_id = client.client_id,
            language_code = language_code,
            lat = lat,
            lng = lng,
            start = start,
            count = count,
        )

        result['posts'] = posts
        result['success'] = True

    #except Exception, e:
    #    status_code = 400
    #    result['error_text'] = str(e)

    client_utils.log_client_action(
        client = client,
        url = 'get_approved_posts.json',
        lat = lat,
        lng = lng,
        request = request,
        result = result,
        success = success,
    )

    return utils.make_response(result, status_code)

@view_config(route_name='flag_post.json')
def flag_post(request):
    result = {'success': False}
    status_code = 200

    #try:
    if True:

        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        #try:
        if True:

            post_id = int(request.POST['post_id'])
            if post_id < 1:
                raise Exception('Invalid input')
            
            post = client_utils.flag_post(
                post_id = post_id,
            )

            result['post_id'] = post.post_id
            result['success'] = True

    #except Exception, e:
    #    status_code = 400
    #    result['error_text'] = str(e)

    return utils.make_response(result, status_code)

@view_config(route_name='register_vote.json')
def register_vote(request):

    result = {'success': False}
    status_code = 200

    try:
        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        try:
            post_id = int(request.POST['post_id'])
            if post_id < 1:
                raise Exception('Invalid input')
            _is_up_vote = int(request.POST['is_up_vote'])
            if _is_up_vote == 1:
                is_up_vote = True
            elif _is_up_vote == 0:
                is_up_vote = False
            else:
                raise Exception('Invalid input.')
        except:
            status_code = 403
            raise Exception("Missing or Invalid input.")

        vote = client_utils.register_vote(
            post_id = post_id,
            client_id = client.client_id,
            is_up_vote = is_up_vote,
        )

        result['vote_id'] = vote.vote_id
        result['post_id'] = vote.post_id
        result['is_up_vote'] = vote.is_up_vote
        result['success'] = True

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    client_utils.log_client_action(
        client = client,
        url = 'register_vote.json',
        lat = lat,
        lng = lng,
        request = request,
        result = result,
        success = success,
    )

    return utils.make_response(result, status_code)


@view_config(route_name='upload_media.json')
def upload_media(request):

    result = {'success': False}
    status_code = 200

    try:
        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        try:
            media_type = request.POST['media_type']
        except:
            raise Exception("Missing media_type field.")

        media_caption = ''
        media_text = ''
        media_object_filename = ''
        media_object_preview_filename = ''

        if media_type == 'image' or media_type == 'video' \
                or media_type == 'audio':

            # Since there is a file being uploaded, we'll need to
            # decode some additional POST params
            try:
                media_file_name = request.POST['media_file'].filename
                input_file = request.POST['media_file'].file
            except:
                raise Exception('Missing of invalid file field.')

            # this is to support legacy android versions.  Should be removed soon.
            try:
                media_caption = request.POST['caption']
            except:
                try:
                    media_caption = request.POST['media_caption']
                except:
                    pass

            base_filename = client_utils.save_input_file(
                input_file = input_file,
            )

            #decode media type of file
            if media_type == 'image':

                image_filename, preview_filename = client_utils.process_image(
                    base_filename = base_filename,
                )

                media_object_filename = image_filename 
                media_object_preview_filename = preview_filename

            #process video files
            elif media_type == 'video':

                video_filename, preview_filename = client_utils.process_video(
                    base_filename = base_filename,
                )

                media_object_filename = video_filename
                media_object_preview_filename = preview_filename

            #process audio files
            elif media_type == 'audio':
                
                audio_filename, preview_filename = client_utils.process_audio(
                    base_filename = base_filename,
                )

                media_object_filename = audio_filename
                media_object_preview_filename = preview_filename

            # cleanup our temp file
            os.remove(base_filename)

        elif media_type == 'text':

            # text isn't an uploaded file, it is within the media_text POST
            # param.
                
            try:
                media_text = request.POST['media_text']
            except:
                 raise Exception('Invalid/missing field')
        else:
            raise Exception('Invalid media type: {0}'.format(media_type))

        media_object = client_utils.add_media_object(
            client_id = client.client_id,
            media_type_text = media_type,
            file_name = os.path.basename(media_object_filename),
            caption = media_caption,
            media_text = media_text,
        )

        result['media_id'] = media_object.media_id
        result['success'] = True

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    client_utils.log_client_action(
        client = client,
        url = 'upload_media.json',
        lat = lat,
        lng = lng,
        request = request,
        result = result,
        success = success,
    )

    return utils.make_response(result, status_code)

@view_config(route_name='publish_post.json')
def publish_post(request):

    result = {'success': False}
    status_code = 200

    try:
        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        try:
            assignment_id = 0
            if 'assignment_id' in request.POST and \
                    request.POST['assignment_id'] != '':
                assignment_id = int(float(str(request.POST['assignment_id'])))
        except:
            status_code = 403
            raise Exception("Invalid input.")

        media_obects = []
        try:
             media_objects = json.loads(urllib.unquote(
                request.POST['media_objects']).decode('utf8')
            )
        except:
            raise Exception("Missing or invalid MediaObjects JSON list.")

        post, vote = client_utils.add_post(
            client_id = client.client_id,
            assignment_id = assignment_id,
            language_code = language_code,
            lat = lat,
            lng = lng,
            media_objects = media_objects,
        )

        result['success'] = True
        result['post_id'] = post.post_id
        result['vote_id'] = vote.vote_id

    except Exception, e:
       status_code = 400
       result['error_text'] = str(e)

    client_utils.log_client_action(
        client = client,
        url = 'publish_post.json',
        lat = lat,
        lng = lng,
        request = request,
        result = result,
        success = success,
    )

    return utils.make_response(result, status_code)


