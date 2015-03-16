'use strict';

angular
    .module('Yellr')
    .controller('writeArticleCtrl',
    ['$scope', '$rootScope', '$location', 'collectionApiService',
    function ($scope, $rootScope, $location, collectionApiService) {

        if (!window.loggedIn) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;
        $scope.$parent.clear();

        $scope.activeNotification = false;
        $scope.createAssignment = false;
        $scope.addQuestions = false;
        $scope.geofence = false;
        $scope.canPublish = false;

    }]);
