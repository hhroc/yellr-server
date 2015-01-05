'use strict';

angular
    .module('Yellr')
    .controller('rawFeedCtrl', ['$scope', function ($scope) {

        /**
         * Populates feed with first 50 items
         *
         * @return void
         */
        $scope.getFeed = function () {
            return [
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '2 hours ago',
                    link: ''
                },
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '2 hours ago',
                    link: ''
                },
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '2 hours ago',
                    link: ''
                },
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '2 hours ago',
                    link: ''
                },
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '2 hours ago',
                    link: ''
                },
            ];
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

        $scope.posts = $scope.getFeed();
        $scope.collections = $scope.getCollections();
    }]);
