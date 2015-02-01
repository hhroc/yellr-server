'use strict';

angular
    .module('Yellr')
    .controller('viewAssignmentsCtrl', ['$scope', '$rootScope', '$location',
                'assignmentApiService',
    function ($scope, $rootScope, $location, assignmentApiService) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        $scope.$parent.clear();
        $scope.$parent.assignmentsPage = true;

        /**
         * Create view assignments function
         *
         * @return void
         */
        function _getAssignments {
            assignmentApiService.getAssignments($scope.user.token)
            .success(function (data) {
                $scope.assignments = data.assignments;
            });
        };

        _getAssignments();

    }]);
