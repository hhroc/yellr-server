'use strict';

angular
    .module('Yellr')
    .controller('viewPostCtrl',
            ['$scope', '$stateParams', '$location', '$rootScope',
                'assignmentApiService',
            function ($scope, $stateParams, $location, $rootScope,
                      assignmentApiService) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        assignmentApiService.getPost($rootScope.user.token, $stateParams.postId)
        .success(function (data) {
            $scope.post = data.post;
        });
    }]);
