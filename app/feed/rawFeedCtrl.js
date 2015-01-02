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
                    time: '11:59pm 01/01/15',
                    link: ''
                },
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '11:59pm 01/01/15',
                    link: ''
                },
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '11:59pm 01/01/15',
                    link: ''
                },
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '11:59pm 01/01/15',
                    link: ''
                },
                {
                    title: 'Post Title',
                    description: 'This is an example of what a preview of the post would be. It would likely be cut off right about here...',
                    time: '11:59pm 01/01/15',
                    link: ''
                },
            ];
        };

        $scope.posts = $scope.getFeed();
    }]);
