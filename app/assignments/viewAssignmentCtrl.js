'use strict';

angular
    .module('Yellr')
    .controller('viewAssignmentCtrl',
    ['$scope', '$stateParams', '$location', '$rootScope', '$modal',
        'assignmentApiService',
    function ($scope, $stateParams, $location, $rootScope, $modal,
              assignmentApiService) {

        if (!window.loggedIn) {
            //$location.path('/login');
            window.location = '/login'; 
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

        $scope.openPost = function (postId) {
            $scope.postId = postId;
            var modalInstance = $modal.open({
                templateUrl: 'assets/templates/viewPost.html',
                controller: 'viewPostModalCtrl',
                scope: $scope
            });
        };

        /**
         * Create view assignments function
         *
         * @return void
         */
        assignmentApiService.getAssignments()
        .success(function (data) {
            $scope.assignment = undefined;
            data.assignments.forEach(function (assignment) {
                if (assignment.id == $stateParams.assignmentId) {
                    console.log('assignment:')
                    console.log(assignment);
                    $scope.assignment = assignment;
                }
            });
        });

        assignmentApiService.getAssignmentResponses($stateParams.assignmentId)
        .success(function (data) {
            $scope.posts = data.posts;
        });

    }]);
