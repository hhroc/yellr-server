'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .controller('rawFeedCtrl',
        ['$scope', '$rootScope', '$location', 'assignmentApiService',
            'collectionApiService',
         function ($scope, $rootScope, $location, assignmentApiService, collectionApiService) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        $scope.$parent.clear();
        $scope.$parent.feedPage = true;

        var _getFirstText = function (post) {
            for (var i = 0; i < post.media_objects.length; i++) {
                var mediaObject = post.media_objects[i];
                if (mediaObject.media_type_name == 'text') {
                    return mediaObject.media_text;
                }
            }

            return null;
        };

        var _getFirstImage = function (post) {
            for (var i = 0; i < post.media_objects.length; i++) {
                var mediaObject = post.media_objects[i];
                if (mediaObject.media_type_name == 'image') {
                    return {
                        'background-image': 'url(/media/' +
                            mediaObject.preview_file_name + ')'
                    };
                }
            }
            return null;
        };

        /**
         * Populates feed with first 50 items
         *
         * @return void
         */
        $scope.getFeed = function () {
            assignmentApiService.getFeed($scope.user.token)
            .success(function (data) {
                var posts = [];
                for (var postId in data.posts) {
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
