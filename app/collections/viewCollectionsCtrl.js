'use strict';

angular
    .module('Yellr')
    .controller('viewCollectionsCtrl',
    ['$scope', '$rootScope', '$location', '$modal', '$templateCache',
        'collectionApiService',
    function ($scope, $rootScope, $location, $modal, $templateCache,
              collectionApiService) {

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        /**
         * Create get collections function
         *
         * @return void
         */
        collectionApiService.getAllCollections($scope.user.token)
        .success(function (data) {
            $scope.collections = data.collections;
        });

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        $scope.$parent.clear();
        $scope.$parent.collectionsPage = true;

        $scope.openModal = function () {
            $modal.open({
                templateUrl: 'assets/templates/newCollectionModal.html',
                controller: 'newCollectionModalCtrl'
            });
        };
    }])

    .controller('newCollectionModalCtrl',
    ['$scope', '$rootScope', '$modalInstance', 'collectionApiService',
    function ($scope, $rootScope, $modalInstance, collectionApiService) {
        $scope.save = function (collection) {
            collectionApiService.createCollection($rootScope.user.token,
                collection.name, collection.description)
            .success(function (data) {
                console.log(data);
            });
        };
    }]);
