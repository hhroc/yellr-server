'use strict';

angular
    .module('Yellr')
    .controller('viewCollectionCtrl',
    ['$scope', '$rootScope', '$location', '$stateParams', '$modal',
        'collectionApiService', 'formatPosts',
    function ($scope, $rootScope, $location, $stateParams, $modal,
              collectionApiService, formatPosts) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;
        $scope.responseTypes = [
            { name: 'All', type: 'all' },
            { name: 'Text Post', type: 'text' },
            { name: 'Image Post', type: 'image' },
            { name: 'Audio Post', type: 'audio' },
            { name: 'Video Post', type: 'video' }
        ];

        $scope.selectedType = 'all';

        $scope.openPost = function (postId) {
            $scope.postId = postId;
            var modalInstance = $modal.open({
                templateUrl: 'assets/templates/viewPost.html',
                controller: 'viewPostModalCtrl',
                scope: $scope
            });
        };

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
            $scope.posts = formatPosts(data.posts);
        });

    }]);
