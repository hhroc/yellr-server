'use strict';

angular
    .module('Yellr')
    .controller('yellrBaseCtrl', ['$scope', function ($scope) {
        $scope.feedPage = false;
        $scope.contributorsPage = false;
        $scope.assignmentsPage = false;
        $scope.collectionsPage = false;
        $scope.messagesPage = false;
        $scope.settingsPage = false;

        $scope.clear = function () {
            $scope.feedPage = false;
            $scope.contributorsPage = false;
            $scope.assignmentsPage = false;
            $scope.collectionsPage = false;
            $scope.messagesPage = false;
            $scope.settingsPage = false;
        };
    }]);
