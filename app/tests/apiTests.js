'use strict';

describe('Calling Access Token API', function () {
    var userApiService, httpBackend,
        username = 'admin',
        correctPassword = 'ABC123ImCorrect',
        wrongPassword = 'XYZ098ImWrong';

    beforeEach(module('Yellr'));
    beforeEach(inject(function (_userApiService_, $httpBackend) {
        userApiService = _userApiService_;
        httpBackend = $httpBackend;

        // Correct response when info is correct
        httpBackend.whenGET('/admin/get_access_token.json?username=' +
            username + '&password=' + correctPassword)
            .respond({
                organization: 'Yellr',
                token: 'c25b7689-8d00-41b6-ad48-dd93d7dcca6f',
                last_name: 'Duffy',
                first_name: 'Timothy',
                success: true
            });


        // Invalid creds response when password is wrong
        httpBackend.whenGET('/admin/get_access_token.json?username=' +
            username + '&password=' + wrongPassword)
            .respond({
                success: false,
                error_text: 'Invalid credentials'
            });
    }));

    it('Should return a successful message when user logs in', function () {
        userApiService.getAccessToken(username, correctPassword).then(
            function(response) {
                expect(response.success).toEqual(true);
            });
    });

    it('Should return a failure when the user logs in with wrong pass',
    function () {
        userApiService.getAccessToken(username, correctPassword).then(
            function(response) {
                expect(response.success).toEqual(false);
            });
    });
});

describe('Calling Post API', function () {
    var token = 'ABC123ImCorrectToken',
        badToken = 'XYZ098ImWrong',
        url = 'admin/get_posts.json?token=',
        badTokenMsg = 'Invalid auth token.',
        missingTokenMsg = 'Missing "token" field in request.',
        assignmentApiService, httpBackend;

    beforeEach(module('Yellr'));
    beforeEach(inject(function (_assignmentApiService_, $httpBackend) {
        assignmentApiService = _assignmentApiService_;
        httpBackend = $httpBackend;

        // Correct request
        httpBackend.whenGET(url + token)
            .respond({
                post_count: 1,
                posts: {
                    '1': {}
                },
                success: true
            });

        // Incorrect Token
        httpBackend.whenGET(url + badToken)
            .respond({
                error_text: badTokenMsg,
                success: false
            });

        httpBackend.whenGET(url)
            .respond({
                error_text: missingTokenMsg,
                success: false
            });
    }));

    it('should return success on normal api call', function () {
        assignmentApiService.getFeed(token)
        .then(function (response) {
            expect(response.success).toEqual(true);
        });
    });

    it('should error due to wrong token', function () {
        assignmentApiService.getFeed(badToken)
        .then(function (response) {
            expect(response.success).toEqual(false);
            expect(response.error_text).toEqual(badTokenMsg);
        });
    });

    it('should error due to no token', function () {
        assignmentApiService.getFeed()
        .then(function (response) {
            expect(response.success).toEqual(false);
            expect(response.error_text).toEqual(missingTokenMsg);
        });
    });
});
