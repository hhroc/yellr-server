'use strict';

angular
    .module('Yellr', ['ui.router', 'mm.foundation'])
    .config(['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/notfound');

        $stateProvider
            .state('login', {
                url: '/login',
                templateUrl: 'assets/templates/login.html',
                controller: 'loginCtrl'
            })
            .state('feed', {
                url: '/feed',
                templateUrl: 'assets/templates/feed.html',
                controller: 'rawFeedCtrl'
            });
    }]);

console.log('Yellr routes');
