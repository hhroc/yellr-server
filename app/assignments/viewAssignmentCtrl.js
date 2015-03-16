'use strict';

angular
    .module('Yellr')
    .controller('viewAssignmentCtrl',
    ['$scope', '$stateParams', '$location', '$rootScope',
        'assignmentApiService', 'formatPosts', 'collectionApiService',
    function ($scope, $stateParams, $location, $rootScope,
              assignmentApiService, formatPosts, collectionApiService) {

        if (!window.loggedIn) {
            $location.path('/login');
            return;
        }

        $scope.responseTypes = [
            { name: 'All', type: 'all' },
            { name: 'Text Post', type: 'text' },
            { name: 'Image Post', type: 'image' },
            { name: 'Audio Post', type: 'audio' },
            { name: 'Video Post', type: 'video' }
        ];
        $scope.selectedType = 'all';

        /**
         * Adds the given post to a collection
         *
         * @return void
         */
        $scope.addPostToCollection = function (post, collection) {
            collectionApiService.addPost(collection.collection_id, post.post_id)
            .success(function (data) {
                collection.post_count++;
            });
        };

        /**
         * Create view assignments function
         *
         * @return void
         */
        assignmentApiService.getAssignments()
        .success(function (data) {
            data.assignments.forEach(function (assignment) {
                if (assignment.assignment_id == $stateParams.assignmentId) {
                    $scope.assignment = assignment;
                }
            });
        });

        assignmentApiService.getAssignmentResponses($stateParams.assignmentId)
        .success(function (data) {
            console.log(formatPosts(data.posts));
            $scope.posts = formatPosts(data.posts);
        });

        collectionApiService.getAllCollections()
        .success(function (data) {

            $scope.collections = data.collections;
        });

    }]);
