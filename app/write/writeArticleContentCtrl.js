'use strict';

var EpicEditor = EpicEditor || {};

angular
    .module('Yellr')
    .controller('writeArticleContentCtrl',
    ['$scope', '$rootScope', '$location', 'collectionApiService',
        'userApiService',
    function ($scope, $rootScope, $location, collectionApiService,
              userApiService) {
        var editor = new EpicEditor().load(),

        _getLanguages = function () {
            userApiService.getLanguages($rootScope.user.token)
            .success(function (data) {
                console.log(data);
                $scope.languages = data.languages;
            });
        };

        _getLanguages();

        /**
         * Gets all images for the current collection
         *
         * @return void
         */
        $scope.getImages = function () {
            $scope.images = [];

            collectionApiService.getPosts($rootScope.user.token,
                $scope.article.collection.collection_id)
            .success(function (data) {
                $scope.$parent.collectionId = $scope.article.collection
                    .collection_id;
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

    }]);
