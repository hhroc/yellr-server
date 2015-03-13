from pyramid.view import view_config

import utils
import admin_utils

@view_config(route_name='admin/get_posts.json')
def admin_get_posts(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

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

        result['posts'] = ret_posts
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/get_post.json')
def admin_get_post(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
        #if True:
            post_id = request.GET['post_id']
        except:
            raise Exception('Missing of invalid field.')

        ret_posts = admin_utils.get_post(post_id)

        result['post'] = ret_posts[0]
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/get_client_posts.json')
def admin_get_client_posts(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            cuid = request.GET['cuid']
        except:
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

        result['posts'] = ret_posts
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/delete_post.json')
def admin_delete_post(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            post_id = request.POST['post_id']
        except:
            raise Exception('Invalid or missing field.')

        post = admin_utils.delete_post(
            post_id = post_id,
        )

        result['post_id'] = post.post_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/approve_post.json')
def admin_approve_post(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            post_id = request.POST['post_id']
        except:
            raise Exception('Invalid or missing field.')

        post = admin_utils.approve_post(
            post_id = post_id,
        )

        result['post_id'] = post.post_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

