(function ($, window, document, undefined) {

  'use strict';


  // ----------------------------------------
  // for testing purposes we'll have this RESPONSES object to test against
  // ----------------------------------------
  var RESPONSES = {
    "posts": [
      {
        "deleted": false,
        "id": "1eaf645f-99ed-4ea0-ba2c-2c0be5faf09b",
        "language_code": "en",
        "down_count": 0,
        "assignment": null,
        "creation_datetime": "2015-10-24 03:45:16",
        "lng": -77.1,
        "flagged": false,
        "lat": 43.5,
        "media_objects": [],
        "up_count": 0,
        "approved": false,
        "contents": "This is a test post!"
      }
    ]
  }


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


      // the things
      // ----------------------------------------
      // console.log(RESPONSES);
      console.log(RESPONSES.posts[0]);

    }

  };



  // initialize the things
  $(document).ready(function () {
    $(document).foundation();
    yellr.init();
  });

}($ || jQuery, window, window.document));
