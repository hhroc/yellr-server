'use strict';

angular
    .module('Yellr')
    .factory('assignmentApiService', ['$http', function ($http) {
        var assignmentApi = {};

        /**
         * Gets all posts submitted to a feed
         *
         * @param accessToken : token needed for all admin functions
         * @param start : (optional) Starting index for results
         * @param count : (optional) Number of results to return.
         * @param reported : (optional) boolean value for including reported
         *                   posts
         * @return posts : http promise containing all posts
         */
        assignmentApi.getFeed = function (accessToken, start, count, reported) {
            var url = '/admin/get_posts.json',
                params = { token: accessToken };

            if(start !== undefined) params.start = start;
            if(count !== undefined) params.start = start;
            if(start !== undefined) params.start = start;


            return $http({
                method: 'GET',
                url: url,
                params: params
            });
        };

        /**
         * Gets all assignments
         *
         * @param accessToken : token needed for all admin functions
         *
         * @return response : response with list of assignments and questions
         */
        assignmentApi.getAssignments = function (accessToken) {
            var url = '/admin/get_assignments.json';

            return  $http({
                method: 'GET',
                url: url,
                params: { token: accessToken }
            });
        };

        /**
         * Creates new question
         *
         * @param accessToken : token needed for all admin functions
         * @param languageCode : 2 letter language code (en, es, etc)
         * @param questionText : Text of question users will see
         * @param description : Addition info on question
         * @param answers : (optional) JSON string of accepted answers
         *
         * @return response : either error or sucess response with question id
         */
        assignmentApi.createQuestion = function (accessToken, languageCode,
                                           questionText, description,
                                           questionType, answers) {
            var url = '/admin/create_question.json?token=' + accessToken,
                params = {
                    language_code: languageCode,
                    question_text: questionText,
                    description: description,
                    question_type: questionType
                };

            if(answers !== undefined) params.answers = answers;

            return $http({
                method: 'POST',
                url: url,
                params: params
            });
        };

        /**
         * Publishes assignment to all users within given GeoBox
         *
         * @param accessToken : token need for all admin functions
         * @param lifeTime : time that assignment will last (hours)
         * @param questions : json array of question ids
         * @param topLeftLat : top left latitude of geobox
         * @param topLeftLng : top left longitude of geobox
         * @param bottomRightLat : bottom right latitude of geobox
         * @param bottomRightLng : bottom right longitude of geobox
         *
         * @return response : either error or sucess response with assignment
         *                    id
         */
        assignmentApi.publishAssignment = function (accessToken, lifeTime, questions,
                                               topLeftLat, topLeftLng,
                                               bottomRightLat, bottomRightLng) {

            var url = '/admin/publish_assignment.json?token=' + accessToken,
                params = {
                    life_time: lifeTime,
                    questions: questions,
                    top_left_lat: topLeftLat,
                    top_left_lng: topLeftLng,
                    bottom_right_lat: bottomRightLat,
                    bottom_right_lng: bottomRightLng
                };


            return $http({
                method: 'POST',
                url: url,
                params: params
            });
        };

        /**
         * Updates assignment to all users within given GeoBox
         *
         * @param accessToken : token need for all admin functions
         * @param lifeTime : time that assignment will last (hours)
         * @param topLeftLat : top left latitude of geobox
         * @param topLeftLng : top left longitude of geobox
         * @param bottomRightLat : bottom right latitude of geobox
         * @param bottomRightLng : bottom right longitude of geobox
         *
         * @return response : either error or success response with assignment
         *                    id
         */
        assignmentApi.updateAssignment = function (accessToken, lifeTime, topLeftLat,
                                              topLeftLng, bottomRightLat,
                                              bottomRightLng) {

            var url = '/admin/update_assignment.json?token=' + accessToken,
                params = {
                    life_time: lifeTime,
                    top_left_lat: topLeftLat,
                    top_left_lng: topLeftLng,
                    bottom_right_lat: bottomRightLat,
                    bottom_right_lng: bottomRightLng
                };


            return $http({
                method: 'POST',
                url: url,
                params: params
            });
        };

        /**
         * Gets all responses for a specific assignment
         *
         * @param accessToken : token needed for all admin functions
         * @param id : Id of assignment to get responses for.
         * @param start : (optional) Starting index for results.
         * @param count : (optional) Number of results to return.
         *                   posts
         * @return posts : http promise containing all responses
         */
        assignmentApi.getAssignmentResponses = function (accessToken, id,
                                                        start, count) {

            var url = '/admin/get_assignment_responses.json?token=' + accessToken,
                params = { assignment_id: id };

            if(start !== undefined) params.start = start;
            if(count !== undefined) params.count = count;

            return $http({
                method: 'POST',
                url: url,
                params: params
            });
        };

        return assignmentApi;
    }]);
