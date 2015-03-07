'use strict';

angular
    .module('Yellr')
    .controller('settingsCtrl',
    ['$scope', '$rootScope', '$location', 'userApiService',
    function ($scope, $rootScope, $location, userApiService) {
        if ($rootScope.user === undefined) {
            $location.path('/login');
            return;
        }

        $scope.user = $rootScope.user;
        $scope.$parent.clear();
        $scope.$parent.settingsPage = true;

        /**
         * Creates a new account
         *
         * @param account : account details - see settings.html for fields
         *
         * @return void
         */
        $scope.newAccount = function (account) {
            userApiService.createUser('moderator', account.userName,
                                      account.password, account.first,
                                      account.last, account.email, 'WXXI')
            .success(function (data) {
                console.log('user created');
            });
        };

        /**
         * Changes the password of the logged in user
         *
         * @param password : form details includes old, new and confirmed
         *                   password.
         */
        $scope.changePassword = function (password) {
            // TODO:
        };
    }]);
