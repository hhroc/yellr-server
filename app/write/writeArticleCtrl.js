'use strict';

var EpicEditor = EpicEditor || {};

angular
    .module('Yellr')
    .controller('writeArticleCtrl',
    ['$scope', '$rootScope', '$location', 'collectionApiService',
    function ($scope, $rootScope, $location, collectionApiService) {

        if($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        var editor = new EpicEditor().load();

        $scope.getImages = function () {
            $scope.images = [];
            console.log($scope.currentCollection.collection_id);
            collectionApiService.getPosts($rootScope.user.token,
                $scope.currentCollection.collection_id)
            .success(function (data) {
                console.log(data);
                _parseImages(data.posts);
            });
        };

        var _parseImages = function (posts) {
            posts.forEach(function (post) {
                post.media_objects.forEach(function (mediaObject) {
                    if(mediaObject.media_type_name == 'image') {

                        mediaObject.markdownLink = '![' + mediaObject.caption +
                            '](/media/' + mediaObject.file_name + ')';
                        $scope.images.push(mediaObject);
                    }
                });
            });
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

    }]);
