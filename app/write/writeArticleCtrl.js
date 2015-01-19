'use strict';

var EpicEditor = EpicEditor || {};

angular
    .module('Yellr')
    .controller('writeArticleCtrl', ['$scope', function ($scope) {
        var editor = new EpicEditor().load();
    }]);
