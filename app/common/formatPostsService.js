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
                    post.contentTypes.push('text');
                    return mediaObject.media_text;
                } else if (mediaObject.media_type_name == 'image') {
                    if ( mediaObject.caption !== '' ) {
                        return mediaObject.caption;
                    }
                }
            }

            return null;
        },
        _getFirstImage = function (post) {
            var i, mediaObject;
            for (i = 0; i < post.media_objects.length; i++) {
                mediaObject = post.media_objects[i];

                if (mediaObject.media_type_name == 'image') {
                    post.contentTypes.push('image');
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
                posts[postId].contentTypes = [];

                posts[postId].time = moment(
                        posts[postId].post_datetime,
                        'YYYY-MM-DD HH:mm:ss')
                    .fromNow();
                posts[postId].text = _getFirstText(
                                                posts[postId]);
                posts[postId].imageUrl = _getFirstImage(
                                                posts[postId]);
            }

            return posts;
        };

        return formatPosts;
    });

