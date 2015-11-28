'use strict';

angular
    .module('Yellr')
    .controller('viewEmbedPostModalCtrl',
    ['$scope', '$rootScope', '$modalInstance', 'assignmentApiService',
    function ($scope, $rootScope, $modalInstance, assignmentApiService) {

        assignmentApiService.getPost($scope.postId)
        .success(function (data) {
            $scope.post = data.post;
        });

    }]);
