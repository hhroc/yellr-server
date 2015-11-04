'use strict';

angular
    .module('Yellr')
    .controller('viewAssignmentCtrl',
    ['$scope', '$stateParams', '$location', '$rootScope', '$modal',
        'assignmentApiService',
    function ($scope, $stateParams, $location, $rootScope, $modal,
              assignmentApiService) {

        if (!window.loggedIn) {
            //$location.path('/login');
            window.location = '/login'; 
            return;
        }

        $scope.responseTypes = [
            { name: 'All', type: 'all' },
            { name: 'Text Post', type: 'text' },
            { name: 'Image Post', type: 'image' },
            { name: 'Audio Post', type: 'audio' },
            { name: 'Video Post', type: 'video' }
        ];
        $scope.selectedType = 'all';

        $scope.openPost = function (postId) {
            $scope.postId = postId;
            var modalInstance = $modal.open({
                templateUrl: 'assets/templates/viewPost.html',
                controller: 'viewPostModalCtrl',
                scope: $scope
            });
        };

        /**
         * Create view assignments function
         *
         * @return void
         */
        assignmentApiService.getAssignments()
        .success(function (data) {
            $scope.assignment = undefined;
            data.assignments.forEach(function (assignment) {
                if (assignment.id == $stateParams.assignmentId) {
                    console.log('assignment:')
                    console.log(assignment);
                    assignment.percents = [
                        {'name': assignment.questions[0].answer0,
                         'index': 'first',
                         'count': assignment.answer0_count,
                         'percent': (assignment.answer0_count / assignment.response_count)*100.0},
                        {'name': assignment.questions[0].answer1,
                         'index': 'second',
                         'count': assignment.answer1_count,
                         'percent': (assignment.answer1_count / assignment.response_count)*100.0},
                        {'name': assignment.questions[0].answer2,
                         'index': 'third',
                         'count': assignment.answer2_count,
                         'percent': (assignment.answer2_count / assignment.response_count)*100.0},
                        {'name': assignment.questions[0].answer3,
                         'index': 'fourth',
                         'count': assignment.answer3_count,
                         'percent': (assignment.answer3_count / assignment.response_count)*100.0},
                        {'name': assignment.questions[0].answer4,
                         'index': 'fifth',
                         'count': assignment.answer4_count,
                         'percent': (assignment.answer4_count / assignment.response_count)*100.0},
                    ];
                    $scope.assignment = assignment;
                }
            });
        });

        assignmentApiService.getAssignmentResponses($stateParams.assignmentId)
        .success(function (data) {
            $scope.posts = data.posts;
        });

    }]);
