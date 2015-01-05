'use strict';

angular
    .module('Yellr', ['ui.router'])
    .config(['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/notfound');

        $stateProvider
            .state('login', {
                url: '/login',
                templateUrl: 'app/templates/login.html',
                controller: 'loginCtrl'
            })
            .state('feed', {
                url: '/feed',
                templateUrl: 'app/templates/feed.html',
                controller: 'rawFeedCtrl'
            });
    }]);

console.log('Yellr routes');
