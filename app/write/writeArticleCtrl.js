'use strict';

angular
    .module('Yellr')
    .controller('writeArticleCtrl', ['$scope', '$rootScope', '$location',
        function ($scope, $rootScope, $location) {

        if($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;
    }]);
