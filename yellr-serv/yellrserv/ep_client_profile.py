from pyramid.view import view_config

import client_utils
import utils

@view_config(route_name='get_profile.json')
def get_profile(request):

    result = {'success': False}
    status_code = 200

    try:
        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        post_count = client_utils.get_profile(
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

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    client_utils.log_client_action(
        client = client,
        url = 'create_response_message.json',
        lat = lat,
        lng = lng,
        request = request,
        result = result,
        success = success,
    )

    return utils.make_response(result, status_code)

@view_config(route_name='verify_client.json')
def verify_user(request):

    result = {'success': False}
    status_code = 200

    try:

        success, error_text, language_code, lat, lng, \
            client = client_utils.register_client(request)
        if success == False:
            raise Exception(error_text)

        #
        # TODO: implement this.  commented out since untested.
        #

        status_code = 501 # not implemented

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

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    return utils.make_response(result, status_code)

