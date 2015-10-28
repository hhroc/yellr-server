'use strict';

angular
    .module('Yellr')
    .factory('assignmentApiService', ['$http', function ($http) {
        var assignmentApi = {};

        /**
         * Gets all posts submitted to a feed
         *
         * @param start : (optional) Starting index for results
         * @param count : (optional) Number of results to return.
         * @param reported : (optional) boolean value for including reported
         *                   posts
         * @return posts : http promise containing all posts
         */
        assignmentApi.getPosts = function (start, count, reported) {
            var url = '/api/admin/posts',
                params = {};

            if (start !== undefined) params.start = start;
            if (count !== undefined) params.count = count;
            if (start !== undefined) params.reported = reported;

            return $http({
                method: 'GET',
                url: url,
                params: params
            });
        };

        /**
         * Gets the contents of a specific post
         *
         * @param id : id of post to get
         *
         * @return post : js object with post data
         */
        assignmentApi.getPost = function (id) {
            var url = '/api/admin/posts/' + id;

            return $http({
                method: 'GET',
                url: url,
            });
        };

        /**
         * Gets all assignments
         *
         * @return response : response with list of assignments and questions
         */
        assignmentApi.getAssignments = function () {
            var url = '/api/assignments';

            return $http({
                method: 'GET',
                url: url
            });
        };

        /**
         * Creates new question
         *
         * @param languageCode : 2 letter language code (en, es, etc)
         * @param questionText : Text of question users will see
         * @param description : Addition info on question
         * @param answers : (optional) JSON string of accepted answers
         *
         * @return response : either error or sucess response with question id
         */
        assignmentApi.createQuestion = function (languageCode,
                                           questionText, description,
                                           questionType, answers) {
            var url = '/api/admin/questions',
                data = {
                    language_code: languageCode,
                    question_text: questionText,
                    description: description,
                    question_type: questionType
                };

            if (answers !== undefined) data.answers = answers;

            return $http({
                method: 'POST',
                url: url,
                data: data,
            });
        };

        /**
         * Publishes assignment to all users within given GeoBox
         *
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
        assignmentApi.publishAssignment = function (name, lifeTime,
                                               questions, topLeftLat, topLeftLng,
                                               bottomRightLat, bottomRightLng) {

            var url = '/api/admin/assignments',
                data = {
                    name: name,
                    life_time: lifeTime,
                    questions: JSON.stringify(questions),
                    top_left_lat: topLeftLat,
                    top_left_lng: topLeftLng,
                    bottom_right_lat: bottomRightLat,
                    bottom_right_lng: bottomRightLng
                };

            return $http({
                method: 'POST',
                url: url,
                data: data
            });
        };

        /**
         * Updates assignment to all users within given GeoBox
         *
         * @param lifeTime : time that assignment will last (hours)
         * @param topLeftLat : top left latitude of geobox
         * @param topLeftLng : top left longitude of geobox
         * @param bottomRightLat : bottom right latitude of geobox
         * @param bottomRightLng : bottom right longitude of geobox
         *
         * @return response : either error or success response with assignment
         *                    id
         */
        assignmentApi.updateAssignment = function (lifeTime, topLeftLat,
                                              topLeftLng, bottomRightLat,
                                              bottomRightLng) {

            var url = '/admin/update_assignment.json',
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
         * @param id : Id of assignment to get responses for.
         * @param start : (optional) Starting index for results.
         * @param count : (optional) Number of results to return.
         *                   posts
         * @return posts : http promise containing all responses
         */
        assignmentApi.getAssignmentResponses = function (id, start, count) {

            var url = '/admin/get_assignment_responses.json',
                params = { assignment_id: id };

            if (start !== undefined) params.start = start;
            if (count !== undefined) params.count = count;

            return $http({
                method: 'POST',
                url: url,
                params: params
            });
        };

        /**
         * Approves the post of a given id
         *
         * @param id : the id of the post to approve
         *
         * @return void
         */
        assignmentApi.approvePost = function (id, post) {
            var url = '/api/admin/posts/' + id,
                data = {
                    approved: !post.approved,
                    deleted: post.deleted,
                    flagged: post.flagged,
                };

            return $http({
                method: 'PUT',
                url: url,
                data: data,
            });
        };

        /**
         * Delete a post from the feed
         *
         * @param id : id of the post to delete
         *
         * @return post_id : id of the deleted post
         */
        assignmentApi.deletePost = function (id, post) {
            var url = '/api/admin/posts/' + id,
                data = {
                    approved: post.approved,
                    flagged: post.flagged,
                    deleted: true,
                };

            return $http({
                method: 'PUT',
                url: url,
                data: data,
            });
        };

        /**
         * Unflag a post from the feed
         *
         * @param id : id of the post to be unflagged
         *
         * @return post_id : id of the unflagged post
         */
        assignmentApi.unflagPost = function (id, post) {
            var url = '/api/admin/posts/' + id,
                data = {
                    approved: post.approved,
                    flagged: false,
                    deleted: post.deleted,
                };

            return $http({
                method: 'PUT',
                url: url,
                data: data,
            });
        }

        /**
         * Registers a post viewed
         *
         * @param id : id of post viewed
         *
         * @return notification_id : id of notification
         */
        assignmentApi.registerPostViewed = function (id) {
            var url = '/admin/register_post_view.json';

            return $http({
                method: 'POST',
                url: url,
                data: $.param({
                    post_id: id
                })
            });
        };

        return assignmentApi;
    }]);
