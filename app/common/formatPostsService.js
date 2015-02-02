'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .factory('formatPosts', function () {
        var _getFirstText = function (post) {
            var i, mediaObject;
            for (i = 0; i < post.media_objects.length; i++) {
                mediaObject = post.media_objects[i];

                if (mediaObject.media_type_name == 'text') {
                    return mediaObject.media_text;
                }
            }

            return null;
        },

        _getFirstImage = function (post) {
            var i, mediaObject;
            for (i = 0; i < post.media_objects.length; i++) {
                mediaObject = post.media_objects[i];

                if (mediaObject.media_type_name == 'image') {
                    return {
                        'background-image': 'url(/media/' +
                            mediaObject.preview_file_name + ')'
                    };
                }
            }
            return null;
        },

        formatPosts = function (posts) {
            for (var postId in posts) {
                // TODO: get title and image
                posts[postId].time = moment(
                        posts[postId].post_datetime,
                        'YYYY-MM-DD HH:mm:ss')
                    .fromNow();
                posts[postId].description = _getFirstText(
                                                posts[postId]);
                posts[postId].imageUrl = _getFirstImage(
                                                posts[postId]);
            }

            return posts;
        };

        return formatPosts;
    });
