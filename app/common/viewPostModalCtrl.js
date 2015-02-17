'use strict';

angular
    .module('Yellr')
    .controller('viewPostModalCtrl',
    ['$scope', '$rootScope', '$modalInstance', 'assignmentApiService',
    function ($scope, $rootScope, $modalInstance, assignmentApiService) {

        console.log($scope);
        assignmentApiService
        .getPost($rootScope.user.token, $scope.postId)
        .success(function (data) {
            console.log('success', data);
            $scope.post = data.post;
        });

    }]);
