'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentCtrl', ['$scope', '$rootScope', '$location',
    function ($scope, $rootScope, $location) {

        if($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        $scope.$parent.clear();
    }]);
