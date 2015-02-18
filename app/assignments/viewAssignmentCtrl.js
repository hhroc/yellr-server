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

        $scope.responseTypes = [
            { name: 'All', type: 'all' },
            { name: 'Text Post', type: 'text' },
            { name: 'Image Post', type: 'image' },
            { name: 'Audio Post', type: 'audio' },
            { name: 'Video Post', type: 'video' }
        ];
        $scope.selectedType = 'all';

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
            console.log(formatPosts(data.posts));
            $scope.posts = formatPosts(data.posts);
        });
    }]);
