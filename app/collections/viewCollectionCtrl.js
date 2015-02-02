'use strict';

angular
    .module('Yellr')
    .controller('viewCollectionCtrl',
    ['$scope', '$rootScope', '$location', '$stateParams',
        'collectionApiService', 'formatPosts',
    function ($scope, $rootScope, $location, $stateParams,
              collectionApiService, formatPosts) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        /**
         * Places collection of url id in scope
         *
         * @return void
         */
        collectionApiService.getAllCollections($scope.user.token)
        .success(function (data) {
            data.collections.forEach(function (collection) {
                if (collection.collection_id == $stateParams.collectionId) {
                    $scope.collection = collection;
                }
            });
        });

        /**
         * Gets all of the posts of the url collection and assigns them into
         * scope.
         *
         * @return void
         */
        collectionApiService.getPosts($rootScope.user.token,
                                      $stateParams.collectionId)
        .success(function (data) {
            console.log(data);
            $scope.posts = formatPosts(data.posts);
        });

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }
    }]);
