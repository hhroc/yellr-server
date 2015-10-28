'use strict';

angular
    .module('Yellr')
    .controller('yellrBaseCtrl',
    ['$scope', '$http', '$rootScope', 'userApiService',
    function ($scope, $http, $rootScope, userApiService) {
        window.loggedIn = false;
        $scope.feedPage = false;
        $scope.assignmentsPage = false;
        $scope.messagesPage = false;
        $scope.settingsPage = false;
        $scope.loading = true;

        $scope.clear = function () {
            $scope.feedPage = false;
            $scope.assignmentsPage = false;
            $scope.messagesPage = false;
            $scope.settingsPage = false;
        };

        userApiService.isLoggedIn()
        .success(function (data) {
            window.loggedIn = data.loggedin;
            $rootScope.user = data;
            $scope.loading = false;
            if (data.loggedin) {
                $('#side-nav').show();
            }
        });
    }]);
