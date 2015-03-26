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
            userApiService.getLanguages()
            .success(function (data) {
                console.log(data);
                $scope.languages = data.languages;
            });
        },

        _getImagesFromPost = function (post) {
            var images = [];

            post.media_objects.forEach(function (mediaObject) {
                if (mediaObject.media_type_name == 'image') {
                    mediaObject.markdownLink = '![' + mediaObject.media_text +
                        '](/media/' + mediaObject.file_name + ')';
                    images.push(mediaObject);
                }
            });

            return images;
        },

        _getQuotesFromPost = function (post) {
            var quotes = [];

            post.media_objects.forEach(function (mediaObject) {
                if (mediaObject.media_type_name == 'text') {
                    quotes.push(mediaObject);
                }
            });

            return quotes;
        };

        $scope.article = $scope.$parent.article;
        if (angular.isDefined($scope.$parent.languages)) {
            $scope.languages = $scope.$parent.languages;
        } else {
            _getLanguages();
        }

        $rootScope.$on('$stateChangeStart',
        function (event, toState, toParams, fromState, fromParams) {
            if (fromState.url == '/write') {
                $scope.$parent.article = $scope.article;
                $scope.$parent.languages = $scope.languages;
                $scope.$parent.article.collection = $scope.article.collection;
            }
        });

        $scope.quotes = [];
        $scope.images = [];

        /**
         * Gets all quotes and images for the current collection
         *
         * @return void
         */
        $scope.getPostContent = function () {
            $scope.quotes = [];
            $scope.images = [];

            collectionApiService
            .getPosts($scope.article.collection.collection_id)
            .success(function (data) {
                $scope.$parent.collectionId = $scope.article.collection
                    .collection_id;

                data.posts.forEach(function (post) {
                    var postQuotes = _getQuotesFromPost(post),
                        postImages = _getImagesFromPost(post);

                    $scope.quotes = $scope.quotes.concat(postQuotes);
                    $scope.images = $scope.images.concat(postImages);
                });
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
                $scope.article.title,
                tags,
                '',
                '',
                content,
                $scope.article.language.code,
                43.5,
                -78,
                43,
                -77
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
        collectionApiService.getAllCollections()
        .success(function (data) {
            $scope.collections = data.collections;
        });

    }]);
