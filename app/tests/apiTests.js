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
        userApiService.login(username, correctPassword).then(
            function (response) {
                expect(response.success).toEqual(true);
            });
    });

    it('Should return a failure when the user logs in with wrong pass',
    function () {
        userApiService.login(username, correctPassword).then(
            function (response) {
                expect(response.success).toEqual(false);
            });
    });
});

describe('Calling Post API', function () {
    var url = 'admin/get_posts.json',
        assignmentApiService, httpBackend;

    beforeEach(module('Yellr'));
    beforeEach(inject(function (_assignmentApiService_, $httpBackend) {
        assignmentApiService = _assignmentApiService_;
        httpBackend = $httpBackend;

        // Correct request
        httpBackend.whenGET(url)
            .respond({
                post_count: 1,
                posts: [
                    {}
                ],
                success: true
            });

    }));

    it('should return success on normal api call', function () {
        assignmentApiService.getPosts()
        .then(function (response) {
            expect(response.success).toEqual(true);
        });
    });

});
