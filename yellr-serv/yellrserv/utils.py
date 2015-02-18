import json
import datetime
from pyramid.response import Response

def make_response(resp_dict, status_code=200):

    print "\n\n[DEBUG]"
    print resp_dict
    print '\n\n'

    resp = Response(json.dumps(resp_dict), content_type='application/json') #, charset='utf8')
    resp.headerlist.append(('Access-Control-Allow-Origin', '*'))

    resp.status = status_code

    return resp

def admin_log(log_text):

    with open('log.txt', 'a') as f:
        f.write('[{0}] {1}\n'.format(str(datetime.datetime.now()),log_text))


