from pyramid.view import view_config

import utils
import admin_utils

import json

@view_config(route_name='admin/get_languages.json')
def admin_get_languages(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        ret_languages = admin_utils.get_languages()

        result['languages'] = ret_languages
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/get_question_types.json')
def admin_get_question_types(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        ret_question_types = admin_utils.get_question_types()

        result['question_types'] = ret_question_types
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/create_question.json')
def admin_create_question(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            language_code = request.POST['language_code']
            question_text = request.POST['question_text']
            description = request.POST['description']
            question_type = request.POST['question_type']
        except:
            raise Exception('Missing or invalid fields.')

        # answers is a json array of strings
        answers = []
        try:
            answers = json.loads(request.POST['answers'])
        except:
            pass

        question = admin_utils.create_question(
            user_id = user.user_id,
            language_code = language_code,
            question_text = question_text,
            description = description,
            question_type = question_type,
            answers = answers,
        )

        result['question_id'] = question.question_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/update_question.json')
def admin_update_question(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            language_code = request.POST['language_code']
            question_text = request.POST['question_text']
            description = request.POST['description']
            question_type = request.POST['question_type']
        except:
            raise Exception('Missing or invalid fields.')

        # answers is a json array of strings
        answers = []
        try:
            answers = json.loads(request.POST['answers'])
        except:
            pass

        # back fill with empty strings
        for i in range(len(answers),10):
            answers.append('')

        question = Questions.update_from_http(
            session = DBSession,
            token = user.token,
            language_code = language_code,
            question_text = question_text,
            description = description,
            question_type = question_type,
            answers = answers,
        )

        result['question_id'] = question.question_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/publish_assignment.json')
def admin_publish_assignment(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            name = request.POST['name']
            life_time = 0
            try:
                life_time = 0
                if 'life_time' in request.POST:
                    life_time = int(float(request.POST['life_time']))
                    if life_time == 0:
                        life_time = 168 # set to 1 week if blank or missing
            except:
                raise Exception("Invalid input.")
            questions = json.loads(request.POST['questions'])
            top_left_lat = float(request.POST['top_left_lat'])
            top_left_lng = float(request.POST['top_left_lng'])
            bottom_right_lat = float(request.POST['bottom_right_lat'])
            bottom_right_lng = float(request.POST['bottom_right_lng'])
        except:
            raise Exception("Missing or invalid fields.")

        assignment, collection = admin_utils.create_assignment(
            user_id = user.user_id,
            name = name,
            life_time = life_time,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
            questions = questions,
        )

        result['assignment_id'] = assignment.assignment_id
        result['collection_id'] = collection.collection_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/update_assignment.json')
def admin_update_assignment(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            assignment_id = request.POST['assignment_id']
            #client_id = request.POST['client_id']
            name = request.POST['name']
            try:
                life_time = 0
                if 'life_time' in request.POST:
                    life_time = int(float(request.POST['life_time']))
                    if life_time == 0:
                        life_time = 168 # set to 1 week if blank or missing
            except:
                raise Exception("Invalid input.")
            #questions = json.loads(request.POST['questions'])
            top_left_lat = float(request.POST['top_left_lat'])
            top_left_lng = float(request.POST['top_left_lng'])
            bottom_right_lat = float(request.POST['bottom_right_lat'])
            bottom_right_lng = float(request.POST['bottom_right_lng'])
        except:
            raise Exception('Missing or invalid fields.')

        # create assignment
        assignment = Assignments.update_assignment(
            session = DBSession,
            assignment_id = assignment_id,
            name = name,
            life_time = life_time,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
            #use_fence = use_fence,
        )

        result['assignment_id'] = assignment.assignment_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)

@view_config(route_name='admin/get_assignments.json')
def admin_get_my_assignments(request):

    result = {'success': False}
    status_code = 200

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            expired = False
            if 'expired' in request.GET:
                expired = False
                if int(request.GET['expired']) == 1:
                    expired = True 
            start = 0
            if 'start' in request.GET:
                start = int(request.GET['start'])
            count = 50
            if 'count' in request.GET:
                count = int(request.GET['count'])
        except:
            status_code = 403
            raise Exception("invalid input")

        ret_assignments = admin_utils.get_assignments(expired, start, count)

        result['assignments'] = ret_assignments
        result['success'] = True

    except Exception, e:
        status_code = 400
        result['error_text'] = str(e)

    return utils.make_response(result, status_code)

@view_config(route_name='admin/get_assignment_responses.json')
def admin_get_assignment_responses(request):

    result = {'success': False}

    try:
        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            assignment_id = int(request.GET['assignment_id'])
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

        deleted=False
        try:
            deleted = bool(int(request.GET['deleted']))
        except:
            pass

        ret_posts = admin_utils.get_response_posts(assignment_id, start, count, deleted)

        result['posts'] = ret_posts
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)


