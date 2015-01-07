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
            })
            .state('assignments', {
                url: '/assignments',
                templateUrl: 'assets/templates/viewAssignments.html',
                controller: 'viewAssignmentsCtrl'
            })
            .state('view-post', {
                url: '/view/:postId',
                templateUrl: 'assets/templates/viewPost.html',
                controller: 'viewPostCtrl'
            });
    }]);

console.log('Yellr routes');
