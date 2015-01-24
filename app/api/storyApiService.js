'use strict';

angular
    .module('Yellr')
    .factory('storyApiService', ['$http', function ($http) {
        var storyApi = {};

        /**
         * publishes given story.
         *
         * @param accessToken : token needed for all admin functions
         * @param title : title of story
         * @param tags : tags associated with story
         * @param topText : place for credit, updates, corrections
         * @param bannerId : media id of banner image
         * @param contents : html content of story
         * @param languageCode : 2 letter code of language
         * @param topLeftLat : top left latitude of geobox
         * @param topLeftLng : top left longitude of geobox
         * @param bottomRightLat : bottom right latitude of geobox
         * @param bottomRightLng : bottom right longitude of geobox
         *
         * @return response : either error code or success with story id
         */
        storyApi.publishStory = function (accessToken, title, tags,
                                              topText, bannerId, contents,
                                              languageCode, topLeftLat,
                                              topLeftLng, bottomRightLat,
                                              bottomRightLng) {

            var url = '/admin/publish_story.json?token=' + accessToken;

            return $http({
                method: 'POST',
                url: url,
                params: {
                    title: title,
                    tags: tags,
                    top_text: topText,
                    banner_media_id: bannerId,
                    contents: contents,
                    language_code: languageCode,
                    top_left_lat: topLeftLat,
                    top_left_lng: topLeftLng,
                    bottom_right_lat: bottomRightLat,
                    bottom_right_lng: bottomRightLng
                }
            });
        };

        /**
         * Register that someone has viewed a specific post/story
         *
         * @param accessToken : token needed for all admin functions
         * @param id : id of story/post being viewed
         *
         * @return response : either error code or success with post id
         */
        storyApi.registerView = function (accessToken, id) {
            var url = '/admin/register_post_view.json?token=' + accessToken;

            return $http({
                method: 'POST',
                url: url,
                params: { post_id: id }
            });
        };

        storyApi.getUserPosts = function (accessToken, id, start, count) {
            var url = '/admin/get_user_posts.json',
                params = {
                    token: accessToken,
                    client_id: id
                };

            if (start !== undefined) params.start = start;
            if (count !== undefined) params.count = count;

            $http({
                method: 'GET',
                url: url,
                params: params
            });
        };


        return storyApi;
    }]);
