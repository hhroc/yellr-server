'use strict';

angular
    .module('Yellr')
    .controller('logoutCtrl',
    ['$location', 'userApiService',
    function ($location, userApiService) {
        // Make logout call
        userApiService.logout()
        .success(function (data) {
            $location.path('/login');
        });
    }]);
