'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .controller('rawFeedCtrl',
        ['$scope', '$rootScope', '$location', 'assignmentApiService',
            'collectionApiService', 'formatPosts',
         function ($scope, $rootScope, $location, assignmentApiService,
                   collectionApiService, formatPosts) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        $scope.$parent.clear();
        $scope.$parent.feedPage = true;

        /**
         * Populates feed with first 50 items
         *
         * @return void
         */
        $scope.getFeed = function () {
            assignmentApiService.getFeed($scope.user.token)
            .success(function (data) {
                var postId,
                    posts = formatPosts(data.posts);

                $scope.posts = posts;
            })
            .error(function (data) {
                console.log('error: ', data);
            });
        };

        /**
         * Gets all current collections
         *
         * @return void
         */
        $scope.getCollections = function () {
            collectionApiService.getAllCollections($scope.user.token)
                .success(function (data) {

                $scope.collections = data.collections;
            });
        };

        /**
         * Adds the given post to a collection
         *
         * @return void
         */
        $scope.addPostToCollection = function (post, collection) {
            console.log(post.post_id, collection.collection_id);
            collectionApiService.addPost($scope.user.token,
                                         collection.collection_id,
                                         post.post_id)
            .success(function (data) {
                console.log(data);
                collection.post_count++;
            });
        };

        /**
         * Deletes a post from the feed
         *
         * @return void
         */
        $scope.deletePost = function (post) {

        };

        $scope.getFeed();
        $scope.getCollections();
    }]);
