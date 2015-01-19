'use strict';

angular
    .module('Yellr')
    .controller('viewAssignmentsCtrl', ['$scope', '$rootScope', '$location',
                'assignmentApiService',
    function ($scope, $rootScope, $location, assignmentApiService) {

        if($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        $scope.$parent.clear();
        $scope.$parent.assignmentsPage = true;

        /**
         * Places all assignments in scope
         *
         * @return void
         */
        $scope.getAssignments = function () {
            assignmentApiService.getAssignments($scope.user.token)
            .success(function (data) {
                $scope.assignments = data.assignments;
            });
        };

        $scope.getAssignments();
    }]);
