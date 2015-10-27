'use strict';

angular
    .module('Yellr')
    .controller('loginCtrl', ['$scope', '$rootScope', '$location',
        'userApiService', function ($scope, $rootScope, $location,
                                    userApiService) {

        var localUser = window.sessionStorage.getItem('YellrUser');

        if (window.loggedIn) {
            $location.path('/feed');
        }

        $scope.error = false;

        /**
         * logs the user in and assigns token in global scope
         *
         * @param username
         * @param password
         */
        $scope.login = function (username, password) {

            userApiService.login(username, password)
            .success(function (data, status, headers, config) {
                window.user = {
                    name: data.first_name + ' ' + data.last_name,
                    organization: data.organization
                };

                if (data.success) {
                    window.loggedIn = true;
                    $location.path('/feed');
                    $('#side-nav').show();
                }
            })

            .error(function (data, status, headers, config) {
                $scope.error = true;
            });
        };
    }]);
