'use strict';

var EpicEditor = EpicEditor || {};

angular
    .module('Yellr')
    .controller('writeArticleContentCtrl',
    ['$scope', '$rootScope', '$location', 'collectionApiService',
        'userApiService', 'storyApiService',
    function ($scope, $rootScope, $location, collectionApiService,
              userApiService, storyApiService) {
        var editor = new EpicEditor().load(),

        _getLanguages = function () {
            userApiService.getLanguages($rootScope.user.token)
            .success(function (data) {
                console.log(data);
                $scope.languages = data.languages;
            });
        };

        _getLanguages();

        $rootScope.$on('$stateChangeStart',
        function (event, toState, toParams, fromState, fromParams) {
            if (fromState.url == '/write') {
                $scope.$parent.article = $scope.article;
                $scope.$parent.article.collection = $scope.article.collection;
            }
            console.log($scope.article);
        });

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
            var content = editor.exportFile(),
                tags = $scope.article.tags.map(function (tag) {
                    return tag.text;
                })
                    .join(',');

            storyApiService.publishStory(
                $rootScope.user.token,
                $scope.article.title,
                tags,
                '',
                '',
                content,
                $scope.article.language.code,
                43.5,
                78,
                43,
                77
            )
            .success(function (data) {
                console.log(data);
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
