from pyramid.view import view_config

import client_utils
import utils

'''
@view_config(route_name='get_notifications.json')
def get_notifications(request):

    result = {'success': False}
    status_code = 200

    try:
    #if True:
        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        notifications = client_utils.get_notifications(
            client_id = client.client_id,
            language_code = language_code,
            lat = lat,
            lng = lng,
        )

        result['notifications'] = notifications
        result['success'] = success

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    client_utils.log_client_action(
        client = client,
        url = 'get_notifications.json',
        lat = lat,
        lng = lng,
        request = request,
        result = result,
        success = success,
    )

    return utils.make_response(result, status_code)

'''
