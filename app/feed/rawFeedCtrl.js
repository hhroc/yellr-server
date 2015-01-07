'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .controller('rawFeedCtrl',
        ['$scope', '$rootScope', '$location', 'assignmentApiService',
            'collectionApiService',
         function ($scope, $rootScope, $location, assignmentApiService, collectionApiService) {

        if($rootScope.user === undefined) {
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
                    var posts = [];
                    for(var postId in data.posts) {
                        // TODO: get title and image
                        data.posts[postId].time = moment(data.posts[postId].post_datetime, 'YYYY-MM-DD HH:mm:ss').fromNow();
                        data.posts[postId].description = $scope.getFirstText(data.posts[postId]);

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

                //TODO: Remove this once #18 is resolved
                data.collections.forEach(function (collection) {
                    collection.numPosts = 0;
                });

                $scope.collections = data.collections;
            });
        };

        /**
         * Adds the given post to a collection
         *
         * @return void
         */
        $scope.addPostToCollection = function(post, collection) {
            console.log(post.post_id, collection.collection_id);
            collectionApiService.addPost($scope.user.token,
                                         collection.collection_id, post.post_id)
                .success(function (data) {

                collection.numPosts++;
            });
        };

        /**
         * Deletes a post from the feed
         *
         * @return void
         */
        $scope.deletePost = function (post) {

        };

        $scope.getFirstText = function (post) {
            for(var i = 0; i < post.media_objects.length; i++) {
                var mediaObject = post.media_objects[i];
                if(mediaObject.media_type_name == 'text') {
                    return mediaObject.media_text;
                }
            }
        };

        $scope.getFeed();
        $scope.getCollections();
    }]);
