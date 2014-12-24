
import json
import requests
import datetime

ROOT_DOMAIN = "http://127.0.0.1:5002/"

def log(output):

    print "[{0}]: {1}".format(str(datetime.datetime.now()).split('.')[0],output) 

def url_action(url, data, method):

    """ 
        url_action(url, data, method)
        
            url = url to send
            data = dict of things to send
            method = 'GET' or 'POST'

    """

    json_response = None
    if True:
    #try:

        if method == 'GET':

            url_payload = "{0}{1}?".format(ROOT_DOMAIN,url)

            for key, value in data.items():
                url_payload += "{0}={1}&".format(key,value)

            http_response = requests.get(url_payload).text
            json_response = json.loads(http_response)

        elif method == 'POST':

            url_payload = "{0}{1}".format(ROOT_DOMAIN,url)

            http_response = requests.post(url_payload, data=data).text

            #print "\n\n"
            #print http_response
            #print "\n\n"

            json_response = json.loads(http_response)

        log("HTTP Response: {0}".format(json_response))

    #except:
    #    pass

    return json_response

def _test_get_access_token(data): #username, password):

    log("----")
    log("TEST: admin/get_access_token.json")
    #log("")

    success = False
    payload = {}

    if True:
    #try:
        url = "admin/get_access_token.json"
        response = url_action(url, data, 'GET')

        if response['success'] == False:
            raise Exception('ERROR: Success = False')

        token = response['token']

        payload['token'] = token

    #except:
    #    pass

    return success, payload

def _test_create_question(token, data): #username, password):

    log("----")
    log("TEST: admin/create_question.json")
    #log("")

    success = False
    payload = {}

    if True:
    #try:
        url = "admin/create_question.json?token={0}".format(token)
        response = url_action(url, data, 'POST')

        if response['success'] == False:
            raise Exception('ERROR: Success = False')

        question_id = response['question_id']

        payload['question_id'] = question_id

    #except:
    #    pass

    return success, payload

def _test_publish_assignment(token, data): #username, password):

    log("----")
    log("TEST: admin/publish_assignment.json")
    #log("")

    success = False
    payload = {}

    if True:
    #try:
        url = "admin/publish_assignment.json?token={0}".format(token)
        response = url_action(url, data, 'POST')

        if response['success'] == False:
            raise Exception('ERROR: Success = False')

        assignment_id = response['assignment_id']

        payload['assignment_id'] = assignment_id

    #except:
    #    pass

    return success, payload

def _test_get_assignments(token, data): #username, password):

    log("----")
    log("TEST: admin/get_my_assignment.json")
    #log("")

    success = False
    payload = {}

    if True:
    #try:
        url = "admin/publish_assignment.json?token={0}".format(token)
        response = url_action(url, data, 'POST')

        if response['success'] == False:
            raise Exception('ERROR: Success = False')

        assignment_id = response['assignment_id']

        payload['assignment_id'] = assignment_id

    #except:
    #    pass

    return success, payload

def run_tests():

    log("Launching tests ...")

    success, payload = _test_get_access_token({
        'username': 'system',
        'password': 'password'}
    )
    token = payload['token']
    log('Got Token: {0}'.format(token))
    log('---\n\n')

    success, payload = _test_create_question(token, {
        'language_code': 'en',
        'question_text': 'How will you be spending New Years Eve?',
        'description': 'Will you be doing anything special for New Years?!?',
        'question_type': 'free_text',
        #'answers': '',
    })
    question_id = payload['question_id']
    log('Question ID: {0}'.format(question_id))
    log('---\n\n')
    
    success, payload = _test_publish_assignment(token, {
        'life_time': 24*7, # 1 week
        'questions': json.dumps([question_id]),
        'top_left_lat': 43.4,
        'top_left_lng': -77.9,
        'bottom_right_lat': 43.0,
        'bottom_right_lng': -77.3,
    })
    assignment_id = payload['assignment_id']
    log('Assignment ID: {0}'.format(assignment_id))
    log('---\n\n')

    success, payload = _test_get_assignments(token, {
        # does not take any fields
    })

if __name__ == '__main__':

    print "\n\n"

    run_tests()
