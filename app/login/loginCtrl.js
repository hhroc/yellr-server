'use strict';

angular
    .module('Yellr')
    .controller('loginCtrl', ['$scope', '$rootScope', '$location',
        'userApiService', function ($scope, $rootScope, $location,
                                    userApiService) {

        var localUser = window.sessionStorage.getItem('YellrUser');

        if(localUser) {
            $rootScope.user = JSON.parse(localUser);
            $location.path('/feed');
        }

        /**
         * logs the user in and assigns token in global scope
         *
         * @param username
         * @param password
         */
        $scope.login = function (username, password) {

            userApiService.getAccessToken(username, password)
            .success(function(data, status, headers, config) {
                $rootScope.user = {
                    name: data.first_name + ' ' + data.last_name,
                    organization: data.organization,
                    token: data.token
                };

                window.sessionStorage.setItem('YellrUser', JSON.stringify($rootScope.user));

                if(data.success) $location.path('/feed');
                else console.log('Login Failure');
            })

            .error(function(data, status, headers, config) {
                // TODO: Handle Error
                console.log('ERROR', data);
            });
        };
    }]);
