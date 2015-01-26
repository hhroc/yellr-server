'use strict';

angular
    .module('Yellr')
    .factory('collectionApiService', ['$http', function ($http) {
        var collectionApi = {};

        /**
         * Gets a list of all current collections
         *
         * @param accessToken : token needed for all admin functions
         *
         * @return collections : list of all collections
         */
        collectionApi.getAllCollections = function (accessToken) {
            var url = '/admin/get_my_collections.json';

            return $http({
                method: 'GET',
                url: url,
                params: {
                    token: accessToken
                }
            });
        };

        /**
         * Creates a new collection.
         *
         * @param accessToken : token needed for all admin functions
         * @param name : name of collection
         * @param description : description of collection
         * @param tags : tags related to collection
         *
         * @return response : either error code or success with collection id
         */
        collectionApi.createCollection = function (accessToken, name, description,
                                              tags) {
            var url = '/admin/create_collection.json?token=' + accessToken;

            return $http({
                method: 'POST',
                url: url,
                params: {
                    name: name,
                    description: description,
                    tags: tags
                }
            });
        };

        /**
         * Disables a collection from use.
         *
         * @param accessToken : token needed for all admin functions
         * @param id : The id of the collection to disable
         *
         * @return response : either error code or success with collection id
         */
        collectionApi.disableCollection = function (accessToken, id) {
            var url = '/admin/disable_collection.json?token=' + accessToken;

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
         * @param accessToken : token needed for all admin functions
         * @param collectionId : id of collection to add to
         * @param postId : id of post to add
         *
         * @return response : either error code or success with collection id
         */
        collectionApi.addPost = function (accessToken, collectionId, postId) {
            var url = '/admin/add_post_to_collection.json?token=' + accessToken;

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
         * @param accessToken : token needed for all admin functions
         * @param collectionId : id of collection to add to
         * @param postId : id of post to add
         *
         * @return response : either error code or success with collection id
         */
        collectionApi.removePost = function (accessToken, collectionId, postId) {
            var url = '/admin/remove_post_from_collection.json?token=' + accessToken;

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
         * @param accessToken : token needed for all admin functions
         * @param id : id of collection to get posts from.
         *
         * @return posts : list of all posts belonging to collection
         */
        collectionApi.getPosts = function (accessToken, id) {
            var url = '/admin/get_collection_posts.json';

            return $http({
                method: 'GET',
                url: url,
                params: {
                    token: accessToken,
                    collection_id: id
                }
            });
        };

        return collectionApi;
    }]);
