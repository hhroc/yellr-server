'use strict';

angular
    .module('Yellr')
    .controller('viewCollectionsCtrl',
    ['$scope', '$rootScope', '$location', '$modal', '$templateCache',
        'collectionApiService',
    function ($scope, $rootScope, $location, $modal, $templateCache,
              collectionApiService) {

        if (!window.loggedIn) {
            //$location.path('/login');
            window.location = '/login';
            return;
        }

        $scope.user = $rootScope.user;
        $scope.$parent.clear();
        $scope.$parent.collectionsPage = true;

        /**
         * Create get collections function
         *
         * @return void
         */
        collectionApiService.getAllCollections()
        .success(function (data) {
            $scope.collections = data.collections;
        });

        $scope.openModal = function () {
            var modalInstance = $modal.open({
                templateUrl: 'assets/templates/newCollectionModal.html',
                controller: 'newCollectionModalCtrl'
            });

            modalInstance.result.then(function (result) {
                $scope.collections.push(result);
            });
        };
    }])

    .controller('newCollectionModalCtrl',
    ['$scope', '$rootScope', '$modalInstance', 'collectionApiService',
    function ($scope, $rootScope, $modalInstance, collectionApiService) {
        $scope.save = function (collection) {
            collectionApiService.createCollection(collection.name,
                                                  collection.description)
            .success(function (data) {
                collection.collection_id = data.collection_id;
                $modalInstance.close(collection);
            });
        };
    }]);
