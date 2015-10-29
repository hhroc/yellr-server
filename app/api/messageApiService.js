'use strict';

angular
    .module('Yellr')
    .factory('messageApiService', ['$http', function ($http) {
        var messageApi = {};

        /**
         * Creates new message to send to another user
         *
         * @param toClientId : ID of client you are messaging
         * @param subject : subject of message
         * @param text : body of message
         * @param parentMessageId : ID of prior message in chain
         *
         * @return response : either error or success response with message id
         */
        messageApi.createMessage = function (toClientId, subject, text,
                                             parentMessageId) {

            var url = '/api/admin/messages',
                params = {
                    to_client_id: toClientId,
                    subject: subject,
                    text: text
                };

            if (parentMessageId !== undefined)
                params.parent_message_id = parentMessageId;

            return $http({
                method: 'POST',
                url: url,
                params: params
            }).error(function(responce){ window.location = '/login'; });
        };

        messageApi.getMessages = function () {
            var url = '/api/admin/messages';

            return $http({
                method: 'GET',
                url: url
            }).error(function(responce){ window.location = '/login'; });
        };

        return messageApi;
    }]);
