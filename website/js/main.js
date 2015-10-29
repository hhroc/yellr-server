/*!
 * yellr-website v0.1.0 (http://yellr.net/)
 */

(function ($, window, document, undefined) {

  'use strict';


  // ----------------------------------------
  // for testing purposes we'll have this RESPONSES object to test against
  // ----------------------------------------
  var RESPONSES = {
    "posts": [
        {
            "has_voted": false,
            "language_code": "en",
            "contents": "This is a test post!",
            "lat": 43.1,
            "assignment": {},
            "is_up_vote": false,
            "id": "72833379-fb27-4471-af08-758e3437be3f",
            "flagged": true,
            "media_objects": [
                {
                    "client_id": "71d7cddc-eddf-4a0a-bea4-eca6f10f1476",
                    "media_type": "image",
                    "filename": "./uploads/71e8524e-39de-4211-80c4-fd19f145f36d.jpg",
                    "creation_datetime": "2015-10-24 18:59:56",
                    "id": "4bd93134-c57f-4e42-9928-0720f79dfa0b",
                    "post_id": "72833379-fb27-4471-af08-758e3437be3f"
                }
            ],
            "lng": -77.5,
            "approved": true,
            "down_count": 0,
            "deleted": false,
            "up_count": 0,
            "creation_datetime": "2015-10-24 18:59:56"
        },
        {
            "has_voted": false,
            "language_code": "en",
            "contents": "This is a test post!",
            "lat": 43.1,
            "assignment": {},
            "is_up_vote": false,
            "id": "de6eda6d-2a1a-456b-8c31-6acf02c80169",
            "flagged": true,
            "media_objects": [
                {
                    "client_id": "71d7cddc-eddf-4a0a-bea4-eca6f10f1476",
                    "media_type": "image",
                    "filename": "./uploads/ae75fda0-7d97-427e-ab2c-97127d6673a2.jpg",
                    "creation_datetime": "2015-10-24 19:00:53",
                    "id": "ba218c0c-e67c-49b6-aa51-cf34734e8da6",
                    "post_id": "de6eda6d-2a1a-456b-8c31-6acf02c80169"
                }
            ],
            "lng": -77.5,
            "approved": true,
            "down_count": 0,
            "deleted": false,
            "up_count": 0,
            "creation_datetime": "2015-10-24 19:00:53"
        },
        {
            "has_voted": false,
            "language_code": "en",
            "contents": "My day is going great, thanks for asking!",
            "lat": 43.1,
            "assignment": {
                "collection_id": "f36bce35-99d8-4438-ad7b-d52691aa611a",
                "top_left_lat": 43.4,
                "bottom_right_lat": 43,
                "bottom_right_lng": -77.3,
                "id": "72b4aa53-c9b9-4725-b8f1-9d9e892457c7",
                "top_left_lng": -77.9,
                "name": "Test Assignment",
                "response_count": 1,
                "questions": [
                    {
                        "question_type": "text",
                        "description": "Tell us about your day so far!",
                        "question_text": "How is your day going?",
                        "language_code": "en",
                        "user_id": "b3b44a7e-7a6b-4835-856c-501020542ee0",
                        "creation_datetime": "2015-10-24 19:00:54",
                        "id": "8cad6588-6572-41da-bebc-d1d87518c5d3"
                    }
                ],
                "author": {
                    "organization": null,
                    "token": "685ea9d6-d0f0-4395-ac65-13a25733334d",
                    "last": "USER",
                    "id": "b3b44a7e-7a6b-4835-856c-501020542ee0",
                    "email": "",
                    "first": "SYSTEM",
                    "token_expire_datetime": "2015-10-25 15:00:54.166735",
                    "user_geo_fence": {
                        "top_left_lat": 90,
                        "bottom_right_lat": -90,
                        "bottom_right_lng": -180,
                        "id": "f58685e7-7e1f-457c-b6c7-71947fe48724",
                        "top_left_lng": 180,
                        "center_lng": 0,
                        "center_lat": 0,
                        "creation_datetime": "2015-10-24 18:59:51"
                    },
                    "username": "system",
                    "creation_datetime": "2015-10-24 18:59:51"
                },
                "creation_datetime": "2015-10-24 19:00:54",
                "expire_datetime": "2015-10-27 15:00:54.456245"
            },
            "is_up_vote": false,
            "id": "1663a56b-fc79-4214-bde7-eca2efdb4e5a",
            "flagged": true,
            "media_objects": [
                {
                    "client_id": "71d7cddc-eddf-4a0a-bea4-eca6f10f1476",
                    "media_type": "image",
                    "filename": "./uploads/9fac3cb0-5ed8-4ef8-b29c-585259d9730d.jpg",
                    "creation_datetime": "2015-10-24 19:00:54",
                    "id": "2f21b910-6ba8-4094-8110-1ce608a3cf17",
                    "post_id": "1663a56b-fc79-4214-bde7-eca2efdb4e5a"
                }
            ],
            "lng": -77.5,
            "approved": true,
            "down_count": 0,
            "deleted": false,
            "up_count": 0,
            "creation_datetime": "2015-10-24 19:00:54"
        }
    ],
    "assignments": [
      {
        "bottom_right_lng": -77.3,
        "top_left_lng": -77.9,
        "id": "1ecec874-74a9-4903-b418-0cedd14c788a",
        "creation_datetime": "2015-10-24 17:49:11",
        "name": "Test Assignment",
        "bottom_right_lat": 43.0,
        "questions": [
          {
            "user_id": "eb86b0d9-1ac3-4e9d-a2bd-63097661712b",
            "question_text": "How is your day going?",
            "id": "061bac8d-1739-4da9-b355-bcfa85bf8710",
            "question_type": "text",
            "creation_datetime": "2015-10-24 17:49:11",
            "description": "Tell us about your day so far!",
            "language_code": "en"
          }
        ],
        "top_left_lat": 43.4,
        "author": {
          "email": "",
          "token": "03e5aa09-d82b-4629-886e-4ee0d6c35ee4",
          "token_expire_datetime": "2015-10-25 13:49:11.466193",
          "username": "system",
          "last": "USER",
          "id": "eb86b0d9-1ac3-4e9d-a2bd-63097661712b",
          "first": "SYSTEM",
          "creation_datetime": "2015-10-24 17:49:05",
          "organization": null,
          "user_geo_fence": {
            "bottom_right_lng": -180.0,
            "top_left_lng": 180.0,
            "top_left_lat": 90.0,
            "id": "557e5dd2-00b7-4c65-9fe9-d099666f5d48",
            "center_lat": 0.0,
            "creation_datetime": "2015-10-24 17:49:05",
            "center_lng": 0.0,
            "bottom_right_lat": -90.0
          }
        },
        "collection_id": "d77c7247-295b-48a4-af42-f610ed4506b8",
        "response_count": 0,
        "expire_datetime": "2015-10-27 13:49:11.855581"
      }
    ]
  };



  window.yellr = {


    tag: 'y e l l r',

    settings: {},

    modules: {},



    utils: {

      /**
       * check if the Drupal object exists
       * @return {boolean}
       */
      drupal_test: function () {
        var drupal_land = false;
        // recon to see if we're in Drupal-land
        if (typeof Drupal !== 'undefined') {
          drupal_land = true;
        }

        return drupal_land;
      },

      /**
       * smooth scroll to a section of the page
       * @return {N/A}
       */
      smooth_scroll: function () {
        // smooth scroll - original source below
        // http://www.learningjquery.com/2007/10/improved-animated-scrolling-script-for-same-page-links
        $('a[data-smooth-scroll]').on('click.smooth_scroll', function() {
          if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
              $('html,body').animate({
                scrollTop: target.offset().top
              }, 1000);

              return false;
            }
          }
        });
      },

      /**
       * Easter egg
       * @return {N/A}
       */
      konami: function () {

        // file urls
        var mp3s = [
          '/misc/internet.mp3',
          '/misc/mario.mp3',
          '/misc/seinfeld.mp3'
        ];
        // file paths are different for Drupal, sites/all/themes/
        if (yellr.utils.drupal_test()) {
          for (var i = 0; i < mp3s.length; i++) {
            mp3s[i] = Drupal.settings.basePath + Drupal.settings.themePath + mp3s[i];
          }
        }

        // load Howler
        if (yellr.sound === undefined) {
          yellr.sound = new Howl({
            urls: [mp3s[Math.floor(Math.random() * 3)]]
          }).play();
        } else {
          // play new sound. stop other one
          yellr.sound.unload();
          yellr.sound = new Howl({
            urls: [mp3s[Math.floor(Math.random() * 3)]]
          }).play();
        }

      }
    },



    init: function() {

      if (console !== undefined) console.log(this.tag);

      // add smooth scroll
      this.utils.smooth_scroll();

      // initialize all modules
      for (var module in this.modules) {
        this.modules[module].init();
      }

      // konami /* play sound effect */
      var easter_egg = new Konami(this.utils.konami);


      // the new things
      // ----------------------------------------
      // console.log(RESPONSES);  // our dummy responses object

      // add dummy posts for now
      // quick and dirty, not yet optimized with a template library or best practices
      console.log('posts');
      var $postsList = $('#posts-list');
      for (var i = 0; i < RESPONSES.posts.length; i++) {
        console.log(RESPONSES.posts[i]);
        var $li = $('<li></li>').addClass('ghost-bg');
        $li.html(RESPONSES.posts[i].contents);
        $postsList.append($li);
      }

      // console.log('assignments');
      // for (var i = 0; i < RESPONSES.assignments.length; i++) {
      //   console.log(RESPONSES.assignments[i]);
      // }

    }

  };



  // initialize the things
  $(document).ready(function () {
    $(document).foundation();
    yellr.init();
  });

}($ || jQuery, window, window.document));

//# sourceMappingURL=main.js.map