'use strict';

angular
    .module('Yellr')
    .controller('viewAssignmentsCtrl',
    ['$scope', '$rootScope', '$location', 'assignmentApiService',
    function ($scope, $rootScope, $location, assignmentApiService) {

        if (!window.loggedIn) {
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
        assignmentApiService.getAssignments()
        .success(function (data) {
            console.log(data);
            $scope.assignments = data.assignments;
        });

    }]);
