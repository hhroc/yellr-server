from pyramid.view import view_config

import client_utils
import utils

@view_config(route_name='get_stories.json')
def get_stories(request):

    result = {'success': False}
    status_code = 200

    try:
    #if True:
        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        start = 0
        count = 25
        try:
            if 'start' in reqeusts.GET:
                start = int(float(request.GET['start']))
            if 'count' in request.GET:
                count = int(float(request.GET['count']))
                if count > 25:
                    # limit the number of stories returned to 25 at a time to 
                    # reduce load on the server
                    count = 25
        except:
            pass

        stories = client_utils.get_stories(
            language_code = language_code,
            lat = lat,
            lng = lng,
            start = start,
            count = count,
        )

        result['stories'] = stories
        result['success'] = True

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    client_utils.log_client_action(
        client = client,
        url = 'get_stories.json',
        lat = lat,
        lng = lng,
        request = request,
        result = result,
        success = success,
    )

    return utils.make_response(result, status_code)

