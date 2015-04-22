'use strict';

angular
    .module('Yellr')
    .controller('yellrBaseCtrl',
    ['$scope', '$http', '$rootScope', 'userApiService',
    function ($scope, $http, $rootScope, userApiService) {
        window.loggedIn = false;
        $scope.feedPage = false;
        $scope.contributorsPage = false;
        $scope.assignmentsPage = false;
        $scope.collectionsPage = false;
        $scope.messagesPage = false;
        $scope.settingsPage = false;
        $scope.loading = true;

        $scope.clear = function () {
            $scope.feedPage = false;
            $scope.contributorsPage = false;
            $scope.assignmentsPage = false;
            $scope.collectionsPage = false;
            $scope.messagesPage = false;
            $scope.settingsPage = false;
        };

        $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

        userApiService.isLoggedIn()
        .success(function (data) {
            window.loggedIn = data.logged_in;
            $rootScope.user = data;
            $scope.loading = false;
            if (data.logged_in) {
                $('#side-nav').show();
            }
        });
    }]);
