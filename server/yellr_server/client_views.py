from pyramid.response import Response
from pyramid.view import view_defaults
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    #DBSession,
    #MyModel,
    Assignments,
    Posts,
    MediaObjects,
    Votes,
    Clients,
    )

import uuid
import os
import subprocess
import magic
import ntpath
import datetime

system_config = {
    'upload_dir': './uploads',
}

def get_payload(request):
    try:
        payload = request.json_body
    except:
        payload = None
    return payload

def build_paging(request):
    start = 0
    count = 50
    if 'start' in request.GET and 'count' in request.GET:
        try:
            start = int(float(request.GET['start']))
            count = int(float(request.GET['count']))
            if count > 50:
                count = 50
        except:
            start = 0
            count = 50
    return start, count


def check_in(request):
    req = (
        'cuid',
        'lat',
        'lng',
        'language_code',
        'platform',
    )
    client = None
    if all(r in request.GET for r in req):
        try:
            cuid = request.GET['cuid']
            lat = float(request.GET['lat'])
            lng = float(request.GET['lng'])
            language_code = request.GET['language_code']
            platform = request.GET['platform'] 
            client = Clients.check_in(
                cuid=cuid, 
                lat=lat,
                lng=lng,
                language_code=language_code,
                platform=platform,
            )
        except:
            pass
    return client


def save_input_file(input_file):

    # generate a unique file name to store the file to
    unique = str(uuid.uuid4())
    filename = os.path.join(system_config['upload_dir'], unique)

    with open(filename, 'wb') as f:
        input_file.seek(0)
        while True:
            data = input_file.read(2<<16)
            if not data:
                break
            f.write(data)

    return filename


def process_image(base_filename):

    image_filename = ""
    preview_filename = ""

    try:

        image_filename = '{0}.jpg'.format(base_filename)
        preview_filename = '{0}p.jpg'.format(base_filename)

        # type incoming file
        mime_type = str(magic.from_file(base_filename, mime=True))
        allowed_image_types = (
            'image/jpeg',
            'image/png',
            'image/x-ms-bmp',
            'image/tiff',
        )

        if not mime_type.lower()[2:-1] in allowed_image_types:
            raise Exception("Unsupported Image Type: %s" % mime_type)

        # convert to jpeg from whatever format it was
        try:
            subprocess.call(['convert', base_filename, image_filename])
        except Exception as ex:
            raise Exception("Error converting image: {0}".format(ex))

        #strip metadata from images with ImageMagick's mogrify
        try:
            subprocess.call(['mogrify', '-strip', image_filename])
        except Exception as ex:
            raise Exception("Error removing metadata: {0}".format(ex))

        # create preview image
        try:
            subprocess.call(['convert', image_filename, '-resize', '400', \
                '-size', '450', preview_filename])
        except Exception as ex:
            raise Exception("Error generating preview image: {0}".format(ex))

    except Exception as ex:
        raise Exception(ex)

    os.remove(base_filename)

    return image_filename, preview_filename


def process_video(base_filename):

    video_filename = ""
    preview_filename = ""

    try:

        # type incoming file
        mime_type = magic.from_file(base_filename, mime=True)
        allowed_image_types = [
            b'video/mpeg',
            b'video/mp4',
            b'video/quicktime',
            b'video/3gpp',
        ]

        if not mime_type.lower() in allowed_image_types:
            raise Exception("Unsupported Image Type: %s" % mime_type)

        video_filename = '{0}.mp4'.format(base_filename)
        preview_filename = '{0}p.jpg'.format(base_filename)

        temp_filename = '{0}.mp4'.format(uuid.uuid4())

        # strip of medta data
        cmd = [
            'ffmpeg',
            '-i',
            base_filename,
            '-map_metadata',
            '-1',
            '-c:v',
            'copy',
            '-c:a',
            'copy',
            temp_filename,
        ]
        print(cmd)
        resp = subprocess.call(cmd)
       
        # convert the video
        cmd = [
            'ffmpeg',
            '-i',
            temp_filename,
            '-strict',
            '-2',
            '-y',
            '-vf',
            'scale=400:trunc(ow/a/2)*2',
            video_filename,
        ]
        print(cmd)
        resp = subprocess.call(cmd)

        # create preview file
        cmd = [
            'ffmpeg',
            '-i',
            video_filename,
            '-ss',
            '00:00:00',
            '-frames:v',
            '1',
            preview_filename,
        ]
        print(cmd)
        resp = subprocess.call(cmd)

        # resize preview file
        cmd = [
            'convert',
            preview_filename,
            '-resize',
            '400',
            '-size',
            '400',
            preview_filename,
        ]
        resp = subprocess.call(cmd)

    except Exception as ex:
        raise Exception(ex)

    os.remove(base_filename)
    os.remove(temp_filename)

    return video_filename, preview_filename


def process_audio(base_filename):

    audio_filename = ""
    preview_filename = ""

    try:

        mime_type = magic.from_file(base_filename, mime=True)
        allowed_audio_types = [
            b'audio/mpeg',
            b'audio/ogg',
            b'audio/x-wav',
            b'audio/mp4',
            b'video/3gpp',
        ]

        if not mime_type.lower() in allowed_audio_types:
            raise Exception("Unsupported Audio Type: %s" % mime_type)

        audio_filename = '{0}.mp3'.format(base_filename)

        cmd = [
            'ffmpeg',
            '-i',
            base_filename,
            '-f',
            'mp3',
            '-map_metadata',
            '-1',
            #'-c:v',
            #'copy',
            #'-c:a',
            #'copy',
            audio_filename,
        ]
        resp = subprocess.call(cmd)

        #
        # Generic audio picture for preview name??
        #

        preview_filename = 'audio_file.png'

    except Exception as ex:
        raise Exception(ex)

    os.remove(base_filename)

    return audio_filename, preview_filename


def humanize(dt):

    now = datetime.datetime.now()
    if dt > now - datetime.timedelta(hours=24):
        resp = dt.strftime('%I%p').replace('0','')
    else:
        resp = dt.strftime('%b %d, %Y')
    return resp

@view_defaults(route_name='/post')
class EmbeddedPost(object):

    def __init__(self, request):
        print('/post')
        self.request = request

    @view_config(request_method='GET', renderer='templates/post.mak')
    def get(self):
        post = None
        if 'id' in self.request.GET:
            post_id = self.request.GET['id']
            post = Posts.get_post_by_id(post_id)
            if post:
                post.human_dt = humanize(post.creation_datetime)
        return {'post': post}


@view_defaults(route_name='/poll')
class EmbeddedPoll(object):

    def __init__(self, request):
        print('/poll')
        self.request = request

    @view_config(request_method='GET', renderer='templates/poll.mak')
    def get(self):
        assignment = None
        if 'id' in self.request.GET:
            assignment_id = self.request.GET['id']
            _assignment = Assignments.get_assignment_by_id(assignment_id)
            if _assignment and _assignment.question_type == 'poll':
                assignment = _assignment
                assignment.percents = [
                    {'name': assignment.questions[0].answer0,
                     'index': 'first',
                     'count': assignment.answer0_count,
                     'percent': (assignment.answer0_count / assignment.response_count)*100.0},
                    {'name': assignment.questions[0].answer1,
                     'index': 'second',
                     'count': assignment.answer1_count,
                     'percent': (assignment.answer1_count / assignment.response_count)*100.0},
                    {'name': assignment.questions[0].answer2,
                     'index': 'third',
                     'count': assignment.answer2_count,
                     'percent': (assignment.answer2_count / assignment.response_count)*100.0},
                    {'name': assignment.questions[0].answer3,
                     'index': 'fourth',
                     'count': assignment.answer3_count,
                     'percent': (assignment.answer3_count / assignment.response_count)*100.0},
                    {'name': assignment.questions[0].answer4,
                     'index': 'fifth',
                     'count': assignment.answer4_count,
                     'percent': (assignment.answer4_count / assignment.response_count)*100.0},
                ]
            print(assignment.percents)
        return {'assignment': assignment}

@view_defaults(route_name='/api/assignments', renderer='json')
class AssignmentsAPI(object):

    def __init__(self, request):
        self.request = request
        start, count = build_paging(request)
        self.client = check_in(request)

    # [ GET ] - get local assignments
    @view_config(request_method='GET')
    def get(self):
        resp = {'assignments': []}
        if self.client:
            start, count = build_paging(self.request)
            _assignments = Assignments.get_all_assignments(
                False,
                self.client.id,
                self.client.last_lat,
                self.client.last_lng,
            )
            resp = {'assignments': [a.to_dict() for a in _assignments]}
        else:
            self.request.response.status = 400
        return resp


@view_defaults(route_name='/api/posts', renderer='json')
class PostsAPI(object):

    post_req = (
        'contents',
        'assignment_id',
        'poll_response',
    )

    def __init__(self, request):
        self.request = request
        self.start, self.count = build_paging(request)
        self.client = check_in(request)

    # [ GET ] - get local posts
    @view_config(request_method='GET')
    def get(self):
        resp = {'posts': []}
        if self.client:
            start, count = build_paging(self.request)
            _posts = Posts.get_approved_posts(
                client_id=self.client.id,
                lat=self.client.last_lat,
                lng=self.client.last_lng,
                start=self.start,
                count=self.count,
            )
            posts = [p.to_dict(self.client.id) for p in _posts]
            resp = {'posts': posts}
        else:
            self.request.response.status = 400
        return resp

    # [ POST ] - create new post
    @view_config(request_method='POST')
    def post(self):
        resp = {'post': None}
        payload = get_payload(self.request)
        if payload and all(r in payload for r in self.post_req) and self.client:
            assignment_id = None
            if payload['assignment_id'] != None:
                assignment_id = payload['assignment_id']
                #print(assignment_id)
                #print('\n\n')
            post = Posts.add(
                client_id=self.client.id,
                assignment_id=assignment_id,
                lat=self.client.last_lat,
                lng=self.client.last_lng,
                language_code=self.client.language_code,
                contents=payload['contents'],
                poll_response=payload['poll_response'],
                deleted=False,
                approved=False,
                flagged=False,
            )
            vote = Votes.register_vote(
                post_id=post.id,
                client_id=self.client.id,
                is_up_vote=True,
            )
            resp = {
                'post': {'id': post.id}, #post.to_dict(self.client.id),
                'vote': {'id': vote.id}, #to_dict(),
            }
        else:
            self.request.response.status = 400
        return resp


@view_defaults(route_name='/api/media_objects', renderer='json')
class MediaObjectsAPI(object):

    post_req = (
        'media_type',
        'post_id',
        'media_file',
    )

    def __init__(self, request):
        self.request = request
        self.client = check_in(request)

    # [ POST ] - creates media object against a post
    @view_config(request_method='POST')
    def post(self):
        resp = {'media_object': None}
        for r in self.post_req:
            try:
                dummy = self.request.POST[r]
                valid = True
            except:
                valid = False
                break
        if valid and self.client:
            if True:
            #try:
                #filename = request.POST['media_file'].filename
                input_file = self.request.POST['media_file'].file
                base_filename = save_input_file(input_file)
                if self.request.POST['media_type'] == 'image':
                    object_filename, preview_filename = process_image(base_filename)
                elif self.request.POST['media_type'] == 'video':
                    object_filename, preview_filename = process_video(base_filename)
                elif self.request.POST['media_type'] == 'audio':
                    object_filename, preview_filename = process_audio(base_filename)
                else:
                    raise Exception('Invalid Media Type')
                media_object = MediaObjects.add(
                    post_id=self.request.POST['post_id'],
                    client_id=self.client.id,
                    media_type=self.request.POST['media_type'],
                    filename=ntpath.basename(object_filename),
                    preview_filename=ntpath.basename(preview_filename),
                )
                resp = {'media_object': media_object.to_dict()}
            #except Exception as ex:
            #    self.request.response.status = 400
            #    resp.update(error = str(ex))
        else:
            self.request.response.status = 400
        return resp


@view_defaults(route_name='/api/posts/{id}/vote', renderer='json')
class VoteAPI(object):

    post_req = (
        'is_up_vote',
    )

    def __init__(self, request):
        self.request = request
        self.client = check_in(request)

    # [ POST ] - votes on a post
    @view_config(request_method='POST')
    def post(self):
        resp = {'vote': None}
        payload = get_payload(self.request)
        if payload and all(r in payload for r in self.post_req) and self.client:
            vote = Votes.register_vote(
                post_id=self.request.matchdict['id'],
                client_id=self.client.id,
                is_up_vote=payload['is_up_vote']
            )
            resp = {'vote': vote.to_dict()}
        else:
            self.request.response.status = 400
        return resp


@view_defaults(route_name='/api/posts/{id}/flag')
class FlagAPI(object):

    post_req = (
        'post_id',
    )

    def __init__(self, request):
        self.request = request
        self.client = check_in(request)

    # [ POST ] - flags a post
    @view_config(request_method='POST')
    def post(self):
        resp = {'post': None}
        payload = get_payload(self.request)
        if payload and all(r in payload for r in self.post_req) and self.client:
            post = Posts.flag_post(
                post_id=payload['post_id'],
            )
            resp = {'post': post.to_dict()}
        else:
            self.request.response.status = 400
        return resp


@view_defaults(route_name='/api/clients', renderer='json')
class ClientsAPI(object):

    def __init__(self, request):
        print('/api/clients')
        self.request = request
        self.client = check_in(request)    

    # [ GET ] - get clients profile
    @view_config(request_method='GET')
    def get(self):
        print('---- start [GET] /api/clients')
        resp = {'client': None}
        if self.client:
            resp = {'client': self.client.to_dict()}
        else:
            self.request.response.status = 400
        print('---- end [GET] /api/clients')
        return resp

    # [ PUT ] - updates a clients profile
    @view_config(request_method='PUT')
    def put(self):
        resp = {}
        return resp

    # [ DELETE ] - marks the client as deleted ( forgotten )
    @view_config(request_method='DELETE')
    def delete(self):
        resp = {}
        
        return resp

