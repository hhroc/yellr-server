'use strict';

angular
    .module('Yellr')
    .controller('writeArticleCtrl', ['$scope', function ($scope) {
        var editor = new EpicEditor().load();
    }]);
