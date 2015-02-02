'use strict';

angular
    .module('Yellr')
    .controller('viewAssignmentCtrl',
    ['$scope', '$stateParams', '$location', '$rootScope',
        'assignmentApiService', 'formatPosts',
    function ($scope, $stateParams, $location, $rootScope,
              assignmentApiService, formatPosts) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        /**
         * Create view assignments function
         *
         * @return void
         */
        assignmentApiService.getAssignments($scope.user.token)
        .success(function (data) {
            data.assignments.forEach(function (assignment) {
                if (assignment.assignment_id == $stateParams.assignmentId) {
                    $scope.assignment = assignment;
                }
            });
        });

        assignmentApiService.getAssignmentResponses($rootScope.user.token,
                                      $stateParams.assignmentId)
        .success(function (data) {
            $scope.posts = formatPosts(data.posts);
        });
    }]);
