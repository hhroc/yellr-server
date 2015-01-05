'use strict';

var moment = moment || {};

angular
    .module('Yellr')
    .controller('rawFeedCtrl',
        ['$scope', '$rootScope', '$location', 'assignmentApiService',
         function ($scope, $rootScope, $location, assignmentApiService) {

        if($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;


        /**
         * Populates feed with first 50 items
         *
         * @return void
         */
        $scope.getFeed = function () {
            console.log('getFeed');
            assignmentApiService.getFeed($scope.user.token)
                .success(function (data) {
                    console.log('getFeed() success: ', data);

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
         * @return collections : All collection objects
         */
        $scope.getCollections = function () {

            return [
                {
                    name: 'Fracking Ban',
                    numPosts: 4,
                },
                {
                    name: 'Urban/Suburban',
                    numPosts: 23,
                },
                {
                    name: 'College Tuition',
                    numPosts: 19
                },
                {
                    name: 'Campaign Finance',
                    numPosts: 102,
                },
            ];
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
        $scope.collections = $scope.getCollections();
    }]);
