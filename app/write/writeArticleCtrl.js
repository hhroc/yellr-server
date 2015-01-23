'use strict';

var EpicEditor = EpicEditor || {};

angular
    .module('Yellr')
    .controller('writeArticleCtrl',
    ['$scope', '$rootScope', '$location', 'collectionApiService',
    function ($scope, $rootScope, $location, collectionApiService) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;
        $scope.$parent.clear();

        $scope.activeNotification = false;
        $scope.createAssignment = false;
        $scope.addQuestions = false;
        $scope.geofence = false;
        $scope.canPublish = false;
        var editor = new EpicEditor().load();

        /**
         * Gets all images for the current collection
         *
         * @return void
         */
        $scope.getImages = function () {
            $scope.images = [];

            collectionApiService.getPosts($rootScope.user.token,
                $scope.currentCollection.collection_id)
            .success(function (data) {
                _parseImages(data.posts);
            });
        };

        /**
         * Publishes the story to the database
         *
         * @return void
         */
        $scope.save = function () {
            var content = editor.exportFile();

            console.log('Content', content);
        };

        /**
         * Gets all collections to populate form with
         *
         * @return void
         */
        collectionApiService.getAllCollections($rootScope.user.token)
        .success(function (data) {
            $scope.collections = data.collections;
        });

        var _parseImages = function (posts) {
            posts.forEach(function (post) {
                post.media_objects.forEach(function (mediaObject) {
                    if (mediaObject.media_type_name == 'image') {

                        mediaObject.markdownLink = '![' + mediaObject.caption +
                            '](/media/' + mediaObject.file_name + ')';
                        $scope.images.push(mediaObject);
                    }
                });
            });
        };

    }]);
