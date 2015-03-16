'use strict';

angular
    .module('Yellr')
    .controller('loginCtrl', ['$scope', '$rootScope', '$location',
        'userApiService', function ($scope, $rootScope, $location,
                                    userApiService) {

        var localUser = window.sessionStorage.getItem('YellrUser');

        if (window.loggedIn) {
            $rootScope.user = JSON.parse(localUser);
            $location.path('/feed');
        }

        /**
         * DEPRECATED
         * logs the user in and assigns token in global scope
         *
         * @param username
         * @param password
         */
        $scope.login = function (username, password) {

            userApiService.getAccessToken(username, password)
            .success(function (data, status, headers, config) {
                $rootScope.user = {
                    name: data.first_name + ' ' + data.last_name,
                    organization: data.organization
                };

                if (data.success) {
                    window.loggedIn = true;
                    $location.path('/feed');
                } else {
                    //TODO
                    console.log('Login Failure');
                }
            })

            .error(function (data, status, headers, config) {
                // TODO: Handle Error
                console.log('ERROR', data);
            });
        };
    }]);
