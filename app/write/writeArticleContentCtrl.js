'use strict';

var EpicEditor = EpicEditor || {};

angular
    .module('Yellr')
    .controller('writeArticleContentCtrl',
        ['$scope', '$rootScope', 'assignmentApiService',
        function ($scope, $rootScope, assignmentApiService) {

        var editor = new EpicEditor().load();
        $scope.images = [];

        var getImages = function () {
            assignmentApiService.getFeed($rootScope.user.token)
            .success(function (data) {
                _parseImages(data.posts);
            });
        };

        var _parseImages = function (posts) {
            posts.forEach(function (post) {
                post.media_objects.forEach(function (mediaObject) {
                    console.log(mediaObject.media_type_name);
                    if(mediaObject.media_type_name == 'image') {

                        mediaObject.markdownLink = '![' + mediaObject.caption +
                            '](/media/' + mediaObject.file_name + ')';
                        $scope.images.push(mediaObject);
                    }
                });
            });
        };

        getImages();
    }]);
