'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .controller('rawFeedCtrl',
    ['$scope', '$rootScope', '$location', '$modal', 'collectionApiService',
     'assignmentApiService', 'formatPosts',
     function ($scope, $rootScope, $location, $modal, collectionApiService,
               assignmentApiService, formatPosts) {
        var postIndex = 0,
            postCount = 50;

        if (!window.loggedIn) {
            //$location.path('/login');
            window.location = '/login';
            return;
        }

        $scope.user = $rootScope.user;
        $scope.feed = true;
        $scope.posts = [];

        $scope.$parent.clear();
        $scope.$parent.feedPage = true;

        $scope.responseTypes = [
            { name: 'All', type: 'all' },
            { name: 'Text Post', type: 'text' },
            { name: 'Image Post', type: 'image' },
            { name: 'Audio Post', type: 'audio' },
            { name: 'Video Post', type: 'video' }
        ];
        $scope.selectedType = 'all';

        $scope.openPost = function (postId) {
            $scope.postId = postId;
            var modalInstance = $modal.open({
                templateUrl: 'assets/templates/viewPost.html',
                controller: 'viewPostModalCtrl',
                scope: $scope
            });
        };

        /**
         * Loads more posts
         *
         * @return void
         */
        $scope.loadMore = function () {
            assignmentApiService.getPosts(postIndex, postCount)
            .success(function (data) {
                console.log(data);
                $scope.posts = $scope.posts.concat(formatPosts(data.posts));
            });
            postIndex += postCount;
        };

        $scope.approvePost = function (post) {
            assignmentApiService.approvePost(post.id, post)
            .success(function (data) {
                post.approved = !post.approved;
                console.log('post approved?', data);
            });
        };
        /**
         * Gets all current collections
         *
         * @return void
         */
        $scope.getCollections = function () {
            collectionApiService.getAllCollections()
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
            collectionApiService.addPost(collection.id, post.id)
            .success(function (data) {
                collection.post_count++;
            });
        };

        /**
         * Deletes a post from the feed
         *
         * @return void
         */
        $scope.deletePost = function (post) {
            assignmentApiService.deletePost(post.id, post)
            .success(function (data) {
                for(var i=0; i<$scope.posts.length; i++) {
                    if ( $scope.posts[i].id == post.id ) {
                        $scope.posts.splice(i,1);
                        break;
                    }
                }
            });
        };

        $scope.loadMore();
        $scope.getCollections();
    }]);
