'use strict';

angular
    .module('Yellr')
    .controller('viewAssignmentCtrl',
    ['$scope', '$stateParams', '$location', '$rootScope',
        'collectionApiService', 'formatPosts',
    function ($scope, $stateParams, $location, $rootScope,
              collectionApiService, formatPosts) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        collectionApiService.getPosts($rootScope.user.token,
                                      $stateParams.collectionId)
        .success(function (data) {
            $scope.posts = formatPosts(data.posts);
        });
    }]);
