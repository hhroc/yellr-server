'use strict';

angular
    .module('Yellr', ['mm.foundation', 'ui.router',
            'ngClipboard', 'ngTagsInput', 'wu.masonry'])
    .config(['$stateProvider', '$urlRouterProvider', 'ngClipProvider',
            function ($stateProvider, $urlRouterProvider, ngClipProvider) {

        ngClipProvider.setPath('assets/js/ZeroClipboard.swf');

        //$urlRouterProvider.otherwise('/login');
        $urlRouterProvider.otherwise('/feed');

        $stateProvider
            .state('logout', {
                url: '/logout',
                controller: 'logoutCtrl'
            })

            .state('feed', {
                url: '/feed',
                templateUrl: 'assets/templates/feed.html',
                controller: 'localFeedCtrl'
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
            .state('view-assignment', {
                url: '/assignments/:assignmentId',
                templateUrl: 'assets/templates/viewAssignment.html',
                controller: 'viewAssignmentCtrl'
            })

            .state('settings', {
                url: '/settings',
                templateUrl: 'assets/templates/settings.html',
                controller: 'settingsCtrl'
            });
    }]);
