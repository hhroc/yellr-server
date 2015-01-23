'use strict';

angular
    .module('Yellr')
    .controller('logoutCtrl', ['$location', function ($location) {
        window.sessionStorage.removeItem('YellrUser');
        $location.path('/login');
    }]);
