'use strict';

angular
    .module('Yellr')
    .factory('collectionApiService', ['$http', function ($http) {
        var collectionApi = {};

        /**
         * Gets a list of all current collections
         *
         * @return collections : list of all collections
         */
        collectionApi.getAllCollections = function () {
            var url = '/admin/get_my_collections.json';

            return $http({
                method: 'GET',
                url: url
            });
        };

        /**
         * Creates a new collection.
         *
         * @param name : name of collection
         * @param description : description of collection
         * @param tags : tags related to collection
         *
         * @return response : either error code or success with collection id
         */
        collectionApi.createCollection = function (name, description,
                                              tags) {
            var url = '/admin/create_collection.json';

            return $http({
                method: 'POST',
                url: url,
                data: $.param({
                    name: name,
                    description: description,
                    tags: tags
                })
            });
        };

        /**
         * Disables a collection from use.
         *
         * @param id : The id of the collection to disable
         *
         * @return response : either error code or success with collection id
         */
        collectionApi.disableCollection = function (id) {
            var url = '/admin/disable_collection.json';

            return $http({
                method: 'POST',
                url: url,
                params: {
                    collection_id: id
                }
            });
        };

        /**
         * Add a post to a collection
         *
         * @param collectionId : id of collection to add to
         * @param postId : id of post to add
         *
         * @return response : either error code or success with collection id
         */
        collectionApi.addPost = function (collectionId, postId) {
            var url = '/admin/add_post_to_collection.json';

            return $http({
                method: 'POST',
                url: url,
                data: $.param({
                    collection_id: collectionId,
                    post_id: postId
                })
            });
        };

        /**
         * Remove a post from a collection
         *
         * @param collectionId : id of collection to add to
         * @param postId : id of post to add
         *
         * @return response : either error code or success with collection id
         */
        collectionApi.removePost = function (collectionId, postId) {
            var url = '/admin/remove_post_from_collection.json';

            return $http({
                method: 'POST',
                url: url,
                params: {
                    collection_id: collectionId,
                    post_id: postId
                }
            });
        };

        /**
         * Gets all posts belonging to a collection
         *
         * @param id : id of collection to get posts from.
         *
         * @return posts : list of all posts belonging to collection
         */
        collectionApi.getPosts = function (id) {
            var url = '/admin/get_collection_posts.json';

            return $http({
                method: 'GET',
                url: url,
                params: {
                    collection_id: id
                }
            });
        };

        return collectionApi;
    }]);
