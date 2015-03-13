from pyramid.view import view_config

import utils
import admin_utils

@view_config(route_name='admin/create_collection.json')
def admin_create_collection(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            name = request.POST['name']
            description = request.POST['description']
            tags = request.POST['tags']
        except:
            raise Exception('Missing or invalid field.')

        collection = admin_utils.create_collection(
            user_id = user.user_id,
            name = name,
            description = description,
            tags = tags,
        )

        result['collection_id'] = collection.collection_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/disable_collection.json')
def admin_disable_collection(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            collection_id = int(request.POST['collection_id'])
        except:
            raise Exception('Missing or invalid field.')

        collection = Collections.disable_collection(
            session = DBSession,
            collection_id = collection_id,
        )

        result['collection_id'] = collection.collection_id
        result['disabled'] = True
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/add_post_to_collection.json')
def admin_add_post_to_collection(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            collection_id = int(request.POST['collection_id'])
            post_id = int(request.POST['post_id'])
        except:
            raise Exception('Missing or invalid field.')

        collection_post = admin_utils.add_post_to_collection(
            collection_id = collection_id,
            post_id = post_id,
        )

        if collection_post is not None:
            result['collection_id'] = collection_post.collection_id
            result['post_id'] = collection_post.post_id
            result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/remove_post_from_collection.json')
def admin_remove_post_from_collection(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            collection_id = int(request.POST['collection_id'])
            post_id = int(request.POST['post_id'])
        except:
            raise Exception('Missing or invalid field.')

        successfully_removed = Collections.remove_post_from_collection(
            session = DBSession,
            collection_id = collection_id,
            post_id = post_id,
        )
        if successfully_removed:
            result['post_id'] = post_id
            result['collection_id'] = collection_id
            result['success'] = True
        else:
            result['error_text'] = 'Post does not exist within collection.'

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/get_collection_posts.json')
def admin_get_collection_posts(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            collection_id = int(request.GET['collection_id'])
        except:
            raise Exception('Missing of invalid field.')

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

        ret_posts = admin_utils.get_collection_posts(
            collection_id = collection_id,
            start = start, 
            count = count,
        )

        result['posts'] = ret_posts
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/get_my_collections.json')
def admin_get_my_collection(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        ret_collections = admin_utils.get_collections(user.user_id)

        result['collections'] = ret_collections
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

