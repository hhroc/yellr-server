from pyramid.view import view_config

import utils
import admin_utils

@view_config(route_name='admin/publish_story.json')
def admin_publish_story(request):

    result = {'success': False}

    try:
    #if True:

        valid, user = admin_utils.check_token(request)
        if valid == False:
            raise Exception("Invalid authorization or bad credentials.")

        try:
            title = request.POST['title']
            tags = request.POST['tags']
            top_text = request.POST['top_text']
            banner_media_id = request.POST['banner_media_id']
            contents = request.POST['contents'].encode('UTF-8')
            top_left_lat = float(request.POST['top_left_lat'])
            top_left_lng = float(request.POST['top_left_lng'])
            bottom_right_lat = float(request.POST['bottom_right_lat'])
            bottom_right_lng = float(request.POST['bottom_right_lng'])
            language_code = request.POST['language_code']
        except:
            raise Exception('Missing of invalid fields.')

        story = admin_utils.create_story(
            user_id = user.user_id,
            title = title,
            tags = tags,
            contents = contents,
            top_left_lat = top_left_lat,
            top_left_lng = top_left_lng,
            bottom_right_lat = bottom_right_lat,
            bottom_right_lng = bottom_right_lng,
            language_code = language_code,
        )
        
        result['story_unique_id'] = story.story_unique_id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return utils.make_response(result)


