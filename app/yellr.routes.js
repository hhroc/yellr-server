'use strict';

angular
    .module('Yellr', ['ui.router'])
    .config(['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/notfound');

        $stateProvider
            .state('feed', {
                url: '/feed',
                templateUrl: '/templates/feed.html',
                controller: 'rawFeedCtrl'
            });
    }]);

console.log('Yellr routes');
