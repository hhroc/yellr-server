'use strict';

angular
    .module('Yellr')
    .controller('loginCtrl', ['$scope', '$rootScope', '$location',
        'userApiService', function ($scope, $rootScope, $location,
                                    userApiService) {

        /**
         * logs the user in and assigns token in global scope
         *
         * @param username
         * @param password
         */
        $scope.login = function (username, password) {
            console.log('login', username, password);

            userApiService.getAccessToken(username, password)
            .success(function(data, status, headers, config) {
                $rootScope.user = {
                    name: data.first_name + ' ' + data.last_name,
                    organization: data.organization,
                    token: data.token
                };

                $location.path('/feed');
            })

            .error(function(data, status, headers, config) {
                // TODO: Handle Error
                console.log(data);
            });
        };
    }]);
