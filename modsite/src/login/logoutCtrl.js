'use strict';

angular
    .module('Yellr')
    .controller('logoutCtrl',
    ['$location', 'userApiService',
    function ($location, userApiService) {
        // Make logout call
        userApiService.logout()
        .success(function (data) {
            window.loggedIn = false;
            //$location.path('/login');
            window.location = '/login';
        })
        .error(function (data) {
            console.log(data);
        });
    }]);
