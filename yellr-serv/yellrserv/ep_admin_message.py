from pyramid.view import view_config

import utils
import admin_utils



@view_config(route_name='admin/create_message.json')
def admin_create_message(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            to_client_id = request.POST['to_client_id']
            subject = request.POST['subject']
            text = request.POST['text']
        except:
            raise Exception('Missing or invalid fields.')

        parent_message_id = None
        try:
            parent_message_id = request.POST['parent_message_id']
        except:
            pass

        message = Messages.create_message_from_http(
            session = DBSession,
            from_token = user.token,
            to_client_id = to_client_id,
            subject = subject,
            text = text,
            parent_message_id = parent_message_id,
        )

        if message != None:
            result['message_id'] = message.message_id
            result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)


