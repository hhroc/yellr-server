from pyramid.view import view_config

import utils
import admin_utils

@view_config(route_name='admin/add_organization.json')
def admin_create_collection(request):

    result = {'success': False}

    try:
    #if True:

        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            name = request.POST['name']
            description = request.POST['description']
            contact_name = request.POST['contact_name']
            contact_email = request.POST['contact_email']
        except:
            raise Exception('Missing or invalid field.')

        organization = admin_utils.create_organization(
            user_type_id = user.user_type_id,
            name = name,
            description = description,
            contact_name = contact_name,
            contact_email = contact_email,
        )

        result['organization_id'] = organization.organization_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/get_organizations.json')
def admin_get_organizations(request):

    result = {'success': False}

    try:
    #if True:

        valid, user = admin_utils.check_token(request)
        if valid == False:
            result['error_text'] = "Missing or invalid 'token' field in request."
            raise Exception('invalid/missing token')

        ret_organizations = admin_utils.get_organizations()

        result['organizations'] = ret_organizations
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/create_user.json')
def admin_create_user(request):

    result = {'success': False}

    try:
    #if True:

        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
        #if True:
            user_type_name = request.POST['user_type']
            user_name = request.POST['username']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            organization_id = request.POST['organization_id']
            fence_top_left_lat = float(request.POST['fence_top_left_lat'])
            fence_top_left_lng = float(request.POST['fence_top_left_lng'])
            fence_bottom_right_lat = float(request.POST['fence_bottom_right_lat'])
            fence_bottom_right_lng = float(request.POST['fence_bottom_right_lng'])
        except:
            raise Exception('Missing or invalid field.')

        new_user = admin_utils.create_user(
             user_type_id = user.user_type_id,
             user_type_name = user_type_name,
             user_name = user_name,
             password = password,
             first_name = first_name,
             last_name = last_name,
             email = email,
             organization_id = organization_id,
             top_left_lat = fence_top_left_lat,
             top_left_lng = fence_top_left_lng,
             bottom_right_lat = fence_bottom_right_lat,
             bottom_right_lng = fence_bottom_right_lng,
        )

        result['user_id'] = new_user.user_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)


