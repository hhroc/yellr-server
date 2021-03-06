from pyramid.view import view_config

import utils
import admin_utils

@view_config(route_name='admin/get_access_token.json')
def admin_get_access_token(request):

    result = {'success': False}
    status_code = 200

    try:
        username = ''
        password = ''
        try:
            username = request.POST['username']
            password = request.POST['password']
            print username
        except:
            raise Exception("Missing of invalid fields.")

        user, org, token, fence = admin_utils.authenticate(username, password)
        if user == None or token == None or fence == None:
            status_code = 403
            raise Exception("Invalid authorization or bad credentials.")


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

        # save the token to the session
        request.session['token'] = token

        result['success'] = True

    except Exception, e:
        if status_code != 403:
            status_code = 400
        result['error'] = str(e)

    return utils.make_response(result, status_code)

@view_config(route_name='admin/check_logged_in.json')
def admin_check_loged_in(request):

    result = {'success': False}

    try:
        
        valid, user, org, fence = admin_utils.check_logged_in(request)

        result['logged_in'] = False
        if valid:

            #result['token'] = token
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

            result['logged_in'] = True

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)


@view_config(route_name='admin/logout.json')
def admin_logout(request):

    result = {'success': False}
    status_code = 200

    try:
        token = None
        try:
            token = request.GET['token']
        except:
            try:
                token = request.session['token']
            except:
                raise Exception("Missing token.")

        if token != None:
            admin_utils.logout(
                token,
            )

            request.session['token'] = ""

        result['success'] = True

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    return utils.make_response(result, status_code)

