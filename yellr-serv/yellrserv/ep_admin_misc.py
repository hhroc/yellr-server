from pyramid.view import view_config

import utils
import admin_utils

@view_config(route_name='admin/register_post_view.json')
def admin_register_post_view(request):

    result = {'success': False}

    try:
    #if True:

        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            post_id = request.POST['post_id']
        except:
            raise Exception('Missing or invalid field.')

        post = Posts.get_from_post_id(
            session = DBSession,
            post_id = post_id,
        )

        notification = Notifications.create_notification(
            session = DBSession,
            user_id = post.user_id,
            notification_type = 'post_viewed',
            payload = json.dumps({
                'organization': user.organization,
            })
        )

        result['post_id'] = post_id
        result['notification_id'] = notification.notification_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return make_response(result)

