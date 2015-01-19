'use strict';

angular
    .module('Yellr')
    .controller('yellrBaseCtrl', ['$scope', '$http', function ($scope, $http) {
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

        $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    }]);
