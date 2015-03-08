#from pyramid.response import Response
from pyramid.view import view_config

#from utils import utils.make_response,
import utils
import admin_utils

@view_config(route_name='admin/get_access_token.json')
def admin_get_access_token(request):

    result = {'success': False}

    try:
    #if True:

        user_name = ''
        password = ''
        try:
            username = request.POST['username']
            password = request.POST['password']

        except:
            result['error_text'] = "Missing 'username' or 'password' within request"
            raise Exception('missing credentials')

        user, org, token, fence = admin_utils.authenticate(username, password)
        if user == None or token == None or fence == None:
            raise Exception('Invalid credentials')

        result['token'] = token
        result['username'] = user.user_name
        result['first_name'] = user.first_name
        result['last_name'] = user.last_name
        result['organization_id'] = org.organization_id
        result['organization'] = org.name

        result['fence'] = {
            'top_left_lat': fence.top_left_lat,
            'top_left_lng': fence.top_left_lng,
            'bottom_right_lat': fence.bottom_right_lat,
            'bottom_right_lng': fence.bottom_right_lng,
        }

        result['success'] = True

    except Exception, e:
        result['error'] = str(e)

    #admin_log("HTTP: admin/get_access_token.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_languages.json')
def admin_get_languages(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        ret_languages = admin_utils.get_languages()

        result['languages'] = ret_languages
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_languages.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_question_types.json')
def admin_get_question_types(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        ret_question_types = admin_utils.get_question_types()

        result['question_types'] = ret_question_types
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_question_types.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_posts.json')
def admin_get_posts(request):

    """ Will return current posts from database """

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        start = 0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count = 50
        try:
            count = int(request.GET['count'])
        except:
            pass

        deleted = False
        try:
            deleted = bool(int(request.GET['deleted']))
        except:
            pass

        ret_posts = admin_utils.get_posts(start, count, deleted)

        #result['total_post_count'] = total_post_count
        result['posts'] = ret_posts

        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_posts.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_assignments.json')
def admin_get_my_assignments(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token what ...')

        start=0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count=50
        try:
            count = int(request.GET['count'])
        except:
            pass

        ret_assignments = admin_utils.get_assignments(start, count)

        #result['assignment_count'] = assignment_count
        result['assignments'] = ret_assignments
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_my_assignments.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_assignment_responses.json')
def admin_get_assignment_responses(request):

    result = {'success': False}

    #if True:
    try:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        try:
            assignment_id = int(request.GET['assignment_id'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        start=0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count=50
        try:
            count = int(request.GET['count'])
        except:
            pass

        deleted=False
        try:
            deleted = bool(int(request.GET['deleted']))
        except:
            pass

        ret_posts = admin_utils.get_response_posts(assignment_id, start, count, deleted)

        #result['post_count'] = post_count
        result['posts'] = ret_posts
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_assignment_responses.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_my_collections.json')
def admin_get_my_collection(request):

    result = {'success': False}

    try:
    #if True:

        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        ret_collections = admin_utils.get_collections(user.user_id)

        result['collections'] = ret_collections
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_my_collections.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_collection_posts.json')
def admin_get_collection_posts(request):

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
            collection_id = int(request.GET['collection_id'])
        except:
            result['error_text'] = "Missing field"
            raise Exception('invalid/missing field')

        start=0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count=50
        try:
            count = int(request.GET['count'])
        except:
            pass

        ret_posts = admin_utils.get_collection_posts(collection_id, start, count)

        #result['post_count'] = post_count
        #result['collection_id'] = collection.collection_id
        #result['collection_name'] = collection.name
        result['posts'] = ret_posts
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_collection_posts.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_user_posts.json')
def admin_get_user_posts(request):

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
            cuid = request.GET['cuid']
        except:
            result['error_text'] = "Missing field"
            raise Exception('Missing or invalid field.')

        start=0
        try:
            start = int(request.GET['start'])
        except:
            pass

        count=50
        try:
            count = int(request.GET['count'])
        except:
            pass

        ret_posts = admin_utils.get_client_posts(cuid, start, count)

        #result['post_count'] = post_count
        result['posts'] = ret_posts
        #result['client_id'] = client_id
        result['success'] = True

    except:
        pass

    #admin_log("HTTP: admin/get_user_posts.json => {0}".format(json.dumps(result)))

    return utils.make_response(result)

@view_config(route_name='admin/get_post.json')
def admin_get_post(request):

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
            post_id = request.GET['post_id']
        except:
            result['error_text'] = "Missing fields"
            raise Exception('missing post_id')

        ret_posts = admin_utils.get_post(post_id)

        result['post'] = ret_posts[0]
        result['success'] = True

    except:
        pass

    return utils.make_response(result)

@view_config(route_name='admin/get_organizations.json')
def admin_get_organizations(request):

    result = {'success': False}

    #try:
    if True:
        token = None
        valid_token = False
        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        ret_organizations = admin_utils.get_organizations()

        result['organizations'] = ret_organizations
        result['success'] = True

    #except:
    #    pass

    return utils.make_response(result)

