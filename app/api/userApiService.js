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
         * https://github.com/hhroc/yellr-server/wiki/API-Documentation#adminget_access_tokenjson
         *
         * @param username : plaintext username of current user
         * @param password : plaintext password of current user (is hashed in
         *                   this function)
         * @return accessToken : http promise of containing token and
         *                       some metadata
         */
        userApi.getAccessToken = function (username, password) {
            var hashedPass = CryptoJS.SHA256(password).toString(),
                url = '/admin/get_access_token.json';

            return $http({
                method: 'POST',
                url: url,
                data: $.param({
                    username: username,
                    password: hashedPass
                })
            });
        };

        /**
         * Creates new user
         *
         * @param accessToken : token needed for all admin functions
         * @param userType : type of user [admin, moderator, etc]
         * @param userName : login id of user
         * @param password : password of user (hashed in this function)
         * @param firstName : first name of user
         * @param lastName : last name of user
         * @param email : email of user
         * @param organization : organization user belongs to
         */
        userApi.createUser = function (userType, userName,
                                      password, firstName, lastName, email,
                                      organization) {
            var url = '/admin/create_user.json',
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

            console.log('params', params);

            return $http({
                method: 'POST',
                url: url,
                data: $.param(params)
            });
        };

        userApi.changePassword = function (username, password) {
            var url = '/admin/change_password.json';

            password = CryptoJS.SHA256(password).toString();

            return $http({
                method: 'POST',
                url: url,
                data: $.param({
                    username: username,
                    password: password
                })
            });
        };

        /**
         * Gets all available languages
         *
         * @param accessToken : token needed for all admin functions
         *
         * @return languages : list of all languages
         */
        userApi.getLanguages = function (accessToken) {
            var url = '/admin/get_languages.json';

            return $http({
                method: 'GET',
                url: url,
                params: { token: accessToken }
            });
        };

        /**
         * Gets all available question types
         *
         * @param accessToken : token needed for all admin functions
         *
         * @return questionTypes : list of all question types
         */
        userApi.getQuestionTypes = function (accessToken) {
            var url = '/admin/get_question_types';

            return $http({
                method: 'GET',
                url: url,
                params: { token: accessToken }
            });
        };

        return userApi;
    }]);
