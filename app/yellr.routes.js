'use strict';

angular
    .module('Yellr', ['ui.router'])
    .config(['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/');

        $stateProvider
            .state('feed', {
                url: '/feed',
                templateUrl: '/templates/feed.html',
                controller: 'rawFeedCtrl'
            });
    }]);
