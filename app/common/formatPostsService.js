'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .factory('formatPosts', function () {
        /*
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
        */

        var _getPostText = function (post) {
            var retText = '';
            var mediaObject = post.media_objects[0];
            if ( mediaObject.media_type_name == 'text' ) {
                retText = mediaObject.media_text;
            }
            else if ( mediaObject.media_type_name == 'image' ) {
                retText = mediaObject.caption;
            }

            if ( retText.length > 128 ) {
                retText = retText.substring(0,128);
            }

            return retText;
        },

        /*
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
        */

        _getPostImage = function(post) {
            var retImage = '';
            var mediaObject = post.media_objects[0];
            if ( mediaObject.media_type_name == 'text' ) {
                retImage = null;
            }
            else if ( mediaObject.media_type_name == 'image' ) {
                retImage = {'background-image': 'url(/media/' +
                            mediaObject.preview_file_name + ')'};
            }
            return retImage;
        },

        formatPosts = function (posts) {
            for (var postId in posts) {
                posts[postId].time = moment(
                        posts[postId].post_datetime,
                        'YYYY-MM-DD HH:mm:ss')
                    .fromNow();
                //posts[postId].description = _getFirstText(
                //                                posts[postId]);
                posts[postId].text = _getPostText(
                                                posts[postId]);
                //posts[postId].imageUrl = _getFirstImage(
                //                                posts[postId]);
                posts[postId].imageUrl = _getPostImage(
                                                posts[postId]);
            }

            return posts;
        };

        return formatPosts;
    });
