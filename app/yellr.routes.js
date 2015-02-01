'use strict';

angular
    .module('Yellr', ['mm.foundation', 'ui.router', 'ui.bootstrap',
            'ngClipboard', 'ngTagsInput', 'wu.masonry'])
    .config(['$stateProvider', '$urlRouterProvider', 'ngClipProvider',
            function ($stateProvider, $urlRouterProvider, ngClipProvider) {

        ngClipProvider.setPath('assets/js/ZeroClipboard.swf');

        $stateProvider
            .state('login', {
                url: '/login',
                templateUrl: 'assets/templates/login.html',
                controller: 'loginCtrl'
            })
            .state('logout', {
                url: '/logout',
                controller: 'logoutCtrl'
            })

            .state('feed', {
                url: '/feed',
                templateUrl: 'assets/templates/feed.html',
                controller: 'rawFeedCtrl'
            })
            .state('view-post', {
                url: '/view/:postId',
                templateUrl: 'assets/templates/viewPost.html',
                controller: 'viewPostCtrl'
            })

            .state('write-article', {
                templateUrl: 'assets/templates/writeArticle.html',
                controller: 'writeArticleCtrl'
            })
            .state('write-article.write', {
                url:'/write',
                templateUrl: 'assets/templates/writeArticleContent.html',
                controller: 'writeArticleContentCtrl'
            })
            .state('write-article.settings', {
                url: '/write/settings',
                templateUrl: 'assets/templates/writeArticleSettings.html',
                controller: 'writeArticleSettingsCtrl'
            })

            .state('new-assignment', {
                templateUrl: 'assets/templates/newAssignment.html',
                controller: 'newAssignmentCtrl'
            })
            .state('new-assignment.content', {
                url: '/new-assignment/content',
                templateUrl: 'assets/templates/newAssignmentContent.html',
                controller: 'newAssignmentContentCtrl'
            })
            .state('new-assignment.questions', {
                url: '/new-assignment/questions',
                templateUrl: 'assets/templates/newAssignmentQuestions.html',
                controller: 'newAssignmentQuestionsCtrl'
            })
            .state('new-assignment.geofence', {
                url: '/new-assignment/geofence',
                templateUrl: 'assets/templates/newAssignmentGeofence.html',
                controller: 'newAssignmentGeofenceCtrl'
            })

            .state('assignments', {
                url: '/assignments',
                templateUrl: 'assets/templates/viewAssignments.html',
                controller: 'viewAssignmentsCtrl'
            })

            .state('collections', {
                url: '/collections',
                templateUrl: 'assets/templates/viewCollections.html',
                controller: 'viewCollectionsCtrl'
            });
    }]);
