'use strict';

angular
    .module('Yellr')
    .controller('rawFeedCtrl', ['$scope', function ($scope) {

        /**
         * Populates feed with first 50 items
         *
         * @return void
         */
        $scope.getFeed = function () {
            console.log('getFeed');
        };

        $scope.getFeed();
    }]);
