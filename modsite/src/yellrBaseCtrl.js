'use strict';

angular
    .module('Yellr')
    .controller('yellrBaseCtrl',
    ['$scope', '$http', '$rootScope', '$location', 'userApiService', 'assignmentApiService',
    function ($scope, $http, $rootScope, $location, userApiService, assignmentApiService) {
        window.loggedIn = false;
        $scope.feedPage = false;
        $scope.assignmentsPage = false;
        $scope.messagesPage = false;
        $scope.settingsPage = false;
        $scope.loading = true;

        $scope.clear = function () {
            $scope.feedPage = false;
            $scope.assignmentsPage = false;
            $scope.messagesPage = false;
            $scope.settingsPage = false;
        };

        $scope.getMediaObjectURL = function(filename) {
            return '/media/' + filename;
        }

        $scope.getMediaObjectPreviewURL = function(preview_filename) {
            return '/media/' + preview_filename;
        }

        userApiService.isLoggedIn()
        .success(function (data) {
            window.loggedIn = data.loggedin;
            $rootScope.user = data;
            $scope.loading = false;
            if (data.loggedin) {
                $('#side-nav').show();
            }
        });
    }]);
