'use strict';

angular
    .module('Yellr')
    .controller('viewCollectionsCtrl',
    ['$scope', '$rootScope', '$location', 'collectionApiService',
    function ($scope, $rootScope, $location, collectionApiService) {

        /**
         * Places all collections in scope
         *
         * @return void
         */
        var _getCollections = function () {
            collectionApiService.getAllCollections($scope.user.token)
            .success(function (data) {
                $scope.collections = data.collections;
            });
        };

        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;

        $scope.$parent.clear();
        $scope.$parent.collectionsPage = true;

        _getCollections();
    }]);
