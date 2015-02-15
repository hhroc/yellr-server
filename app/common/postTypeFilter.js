'use strict';

angular
    .module('Yellr')
    .filter('postType', function () {
        return function (posts, type) {
            var filtered = [];

            if (type == 'all') {
                return posts;
            }

            posts.forEach(function (post) {
                if (post.contentTypes.indexOf(type) !== -1) {
                    filtered.push(post);
                }
            });

            return filtered;
        };
    });
