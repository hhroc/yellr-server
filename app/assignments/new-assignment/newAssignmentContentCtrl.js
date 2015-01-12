'use strict';

angular
    .module('Yellr')
    .controller('newAssignmentContentCtrl', ['$scope', '$timeout',
    function ($scope, $timeout) {
        $scope.format = 'dd-MMMM-yyyy';
        $scope.dateOptions = {
            formatYear: 'yy',
            startingDay: 1
        };

        $scope.save = function (assignment) {
            angular.extend($scope.$parent.assignment, assignment);
            $scope.$parent.notificationMessage = 'Saved Assignment Information';
            $scope.$parent.activeNotification = true;

            $timeout(function () {
                $scope.$parent.activeNotification = false;
            }, 1200);
        };
    }]);
