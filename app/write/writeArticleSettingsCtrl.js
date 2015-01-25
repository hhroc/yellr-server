'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .controller('writeArticleSettingsCtrl',
        ['$scope', '$rootScope', 'collectionApiService',
        function ($scope, $rootScope, collectionApiService) {

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

        _getPosts = function () {
            collectionApiService.getPosts($rootScope.user.token,
                                          $scope.$parent.collectionId)
            .success(function (data) {
                var postId,
                    posts = [];

                for (postId in data.posts) {
                    // TODO: get title and image
                    data.posts[postId].time = moment(
                            data.posts[postId].post_datetime,
                            'YYYY-MM-DD HH:mm:ss')
                        .fromNow();
                    data.posts[postId].description = _getFirstText(
                                                    data.posts[postId]);
                    data.posts[postId].imageUrl = _getFirstImage(
                                                    data.posts[postId]);

                    posts.push(data.posts[postId]);
                }

                $scope.posts = posts;
            });
        };

        _getPosts();
    }]);
