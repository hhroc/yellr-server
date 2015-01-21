'use strict';

angular
    .module('Yellr')
    .controller('writeArticleSettingsCtrl',
        ['$scope', '$rootScope', 'collectionApiService',
        function ($scope, $rootScope, collectionApiService) {

        /**
         * Gets all collections to populate form with
         *
         * @return void
         */
        collectionApiService.getAllCollections($rootScope.user.token)
        .success(function (data) {
            $scope.collections = data.collections;
        });
    }]);
