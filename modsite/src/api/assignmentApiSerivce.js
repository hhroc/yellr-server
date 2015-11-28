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
            }).error(function(response){ window.location = '/login'; });
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
            }) /*.error(function(response){ window.location = '/login'; });*/
        };

        /**
         * Gets all assignments
         *
         * @return response : response with list of assignments and questions
         */
        assignmentApi.getAssignments = function () {
            var url = '/api/admin/assignments';

            return $http({
                method: 'GET',
                url: url
            }).error(function(response){ window.location = '/login'; });
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
        /*
        assignmentApi.createQuestion = function (assignmentid, languageCode,
                                           questionText, description,
                                           questionType, answer0, answer1,
                                           answer2, answer3, answer4) {
            var url = '/api/admin/questions',
                data = {
                    assignment_id: assignment_id,
                    language_code: languageCode,
                    question_text: questionText,
                    description: description,
                    question_type: questionType
                };

            if (answer0 !== undefined) data.answer0 = answer0;
            if (answer1 !== undefined) data.answer1 = answer1;
            if (answer2 !== undefined) data.answer2 = answer2;
            if (answer3 !== undefined) data.answer3 = answer3;
            if (answer4 !== undefined) data.answer4 = answer4;

            return $http({
                method: 'POST',
                url: url,
                data: data,
            }).error(function(response){ window.location = '/login'; });
        };
        */

        /**
         * Publishes assignment to all users within given GeoBox
         *
         * @param name :  name of the assignment
         * @param lifeTime : time that assignment will last (hours)
         * @param questions : json array of question ids
         * @param topLeftLat : top left latitude of geobox
         * @param topLeftLng : top left longitude of geobox
         * @param bottomRightLat : bottom right latitude of geobox
         * @param bottomRightLng : bottom right longitude of geobox
         * @param question_type : either 'text' or 'poll'
         *
         * @return response : either error or sucess response with assignment
         *                    id
         */
        assignmentApi.publishAssignment = function (assignment) {
                                               //name, lifeTime,
                                               //questions, topLeftLat, topLeftLng,
                                               //bottomRightLat, bottomRightLng,
                                               //question_type) {

            var url = '/api/admin/assignments',
                data = {
                    name: assignment.name,
                    life_time: assignment.lifeTime,
                    //questions: JSON.stringify(questions),
                    top_left_lat: assignment.geofence.topLeft.lat, //topLeftLat,
                    top_left_lng: assignment.geofence.topLeft.lng, //topLeftLng,
                    bottom_right_lat: assignment.geofence.bottomRight.lat,
                    bottom_right_lng: assignment.geofence.bottomRight.lng,
                    question_type: assignment.question_type
                };
                console.log('assignmentApi.publishAssignment()');
                console.log(assignment);
                console.log(data);
            return $http({
                method: 'POST',
                url: url,
                data: data
            }).success(function(response) {
                console.log('assignmentApi.publishAssignment.success()');
                console.log(assignment);
                assignment.questions.forEach(function(question) {
                    /*
                    q = assignmentApi.creationQuestion(
                        response.assignment.id,
                        question.languageCode,
                        question.questionText,
                        question.description,
                        question.questionType,
                        question.answer0,
                        question.answer1,
                        question.answer2,
                        question.answer3,
                        question.answer4
                    );
                    */
                    console.log('question:');
                    console.log(question);
                    var url = '/api/admin/questions',
                        data = {
                            assignment_id: response.assignment.id,
                            language_code: question.languageCode,
                            question_text: question.questionText,
                            description: question.description,
                            question_type: question.questionType,
                            answer0: '',
                            answer1: '',
                            answer2: '',
                            answer3: '',
                            answer4: ''
                        };
                    console.log('post question data:');
                    console.log(data);

                    if (question.answer0 !== undefined) data.answer0 = question.answer0;
                    if (question.answer1 !== undefined) data.answer1 = question.answer1;
                    if (question.answer2 !== undefined) data.answer2 = question.answer2;
                    if (question.answer3 !== undefined) data.answer3 = question.answer3;
                    if (question.answer4 !== undefined) data.answer4 = question.answer4;

                    console.log('post question data:');
                    console.log(data);

                    return $http({
                        method: 'POST',
                        url: url,
                        data: data,
                    }).error(function(response){ console.log('add question error: '); console.log(response); /*window.location = '/login';*/ });

                });
            }); //.error(function(response){ window.location = '/login'; });
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
        assignmentApi.updateAssignment = function (id, name, lifeTime, topLeftLat,
                                              topLeftLng, bottomRightLat,
                                              bottomRightLng) {

            var url = '/api/admin/assignments/' + id,
                params = {
                    name: name,
                    life_time: lifeTime,
                    top_left_lat: topLeftLat,
                    top_left_lng: topLeftLng,
                    bottom_right_lat: bottomRightLat,
                    bottom_right_lng: bottomRightLng
                };

            return $http({
                method: 'PUT',
                url: url,
                params: params
            }).error(function(response){ window.location = '/login'; });
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

            var url = '/api/admin/assignments/' + id + '/responses';

            if (start !== undefined && count !== undefined) url += ('?start=' + start + '&count=' + count);

            return $http({
                method: 'GET',
                url: url,
                //params: params
            }).error(function(response){ window.location = '/login'; });
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
            }).error(function(response){ window.location = '/login'; });
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
            }).error(function(response){ window.location = '/login'; });
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
            }).error(function(response){ window.location = '/login'; });
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
            }).error(function(response){ window.location = '/login'; });
        };

        return assignmentApi;
    }]);
