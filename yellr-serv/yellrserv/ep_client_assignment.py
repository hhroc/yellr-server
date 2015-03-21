from pyramid.view import view_config

import client_utils
import utils

@view_config(route_name='get_assignments.json')
def get_assignments(request):

    result = {'success': False}
    status_code = 200

    try:
        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        assignments = client_utils.get_assignments(
            client_id = client.client_id,
            language_code = language_code,
            lat = lat,
            lng = lng,
        )

        result['assignments'] = assignments
        result['success'] = True

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    client_utils.log_client_action(
        client = client,
        url = 'get_assignments.json',
        lat = lat,
        lng = lng,
        request = request,
        result = result,
        success = success,
    )

    return utils.make_response(result, status_code)


