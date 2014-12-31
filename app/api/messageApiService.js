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
        messageApi.createMessage = function (accessToken, toClientId, subject,
                                          text, parentMessageId) {

            var url = '/admin/create_message.json?token=' + accessToken,
                params = {
                    to_client_id: toClientId,
                    subject: subject,
                    text: text
                };

            if(parentMessageId !== undefined)
                params.parent_message_id = parentMessageId;

            return $http({
                method: 'POST',
                url: url,
                params: params
            });
        };

        messageApi.getMessages = function (accessToken) {
            var url = '/admin/get_my_messages.json';

            return $http({
                method: 'GET',
                url: url,
                params: { token: accessToken }
            });
        };

        return messageApi;
    }]);
