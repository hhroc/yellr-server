'use strict';

var CryptoJS = CryptoJS || {};

angular
    .module('Yellr')
    .factory('userApiService', ['$http', function ($http) {
        var userApi = {};

        /**
         * This gets an access token that needs to be passed around with all
         * admin api calls.
         *
         * @param username : plaintext username of current user
         * @param password : plaintext password of current user (is hashed in
         *                   this function)
         * @return DEPRECATED
         */
        userApi.login = function (username, password) {
            var hashedPass = CryptoJS.SHA256(password).toString(),
                url = '/api/admin/login';

            return $http({
                method: 'POST',
                url: url,
                data: {
                    username: username,
                    password: hashedPass
                }
            });
        };

        /**
         * Logs the user out
         */
        userApi.logout = function () {
            var url = '/api/admin/logout';

            return $http({
                method: 'POST',
                url: url
            });
        };

        /**
         * checks if the user is logged in
         *
         * @return response - object with "logged_in" as answer
         */
        userApi.isLoggedIn = function () {
            var url = '/api/admin/login';

            return $http({
                method: 'GET',
                url: url
            });
        };

        /**
         * Creates new user
         *
         * @param userType : type of user [admin, moderator, etc]
         * @param userName : login id of user
         * @param password : password of user (hashed in this function)
         * @param firstName : first name of user
         * @param lastName : last name of user
         * @param email : email of user
         * @param organization : organization user belongs to
         */
        userApi.createUser = function (userType, userName, password, firstName,
                                       lastName, email, organization) {
            var url = '/admin/users',
                params = {
                    user_type: userType,
                    username: userName,
                    password: password,
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    organization_id: 1,
                    fence_top_left_lat: 43,
                    fence_top_left_lng: -77.9,
                    fence_bottom_right_lat: 43.4,
                    fence_bottom_right_lng: -77.3
                };

            params.password = CryptoJS.SHA256(password).toString();

            return $http({
                method: 'POST',
                url: url,
                data: $.param(params)
            }).error(function(response){ window.location = '/login'; });
        };

        userApi.changePassword = function (username, oldPassword, newPassword) {
            var url = '/api/admin/users';

            oldPassword = CryptoJS.SHA256(oldPassword).toString();
            newPassword = CryptoJS.SHA256(newPassword).toString();

            return $http({
                method: 'PUT',
                url: url,
                data: $.param({
                    username: username,
                    old_password: oldPassword,
                    new_password: newPassword
                })
            }).error(function(response){ window.location = '/login'; });
        };

        return userApi;
    }]);
