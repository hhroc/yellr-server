module.exports = function(grunt) {

  'use strict';
  grunt.util.linefeed = '\n';  // Force use of Unix newlines

  // project directory layout
  // ============================================================
  var project = {

    // configuration
    // ----------------------------------------
    images_dir: 'images/',
    jade_dir: 'jade/',
    js_files: [
      'js/frontpage/init.js',
    ],
    js_vendor_files: [
      'bower_components/modernizr/modernizr.js',
      'bower_components/fastclick/lib/fastclick.js',
      'bower_components/jquery/dist/jquery.min.js',
      'bower_components/foundation/js/foundation.min.js',
      'bower_components/howler.js/howler.min.js',
      'bower_components/konami-js/konami.js',
      'bower_components/konami-js/konami.js',
      'bower_components/moment/min/moment.min.js',
      'bower_components/plyr/dist/plyr.js'
    ],
    misc_dir: 'misc/',
    sass_dir: 'scss/',
    sass_filename: 'style.scss',

    // build output
    // ----------------------------------------
    output: {
      folder:                 './',
      html_folder:                'html/',
      css_folder:                 'css/',
      css_filename:                   'style.css',
      css_filename_minified:          'style.min.css',
      js_folder:                  'js/',
      js_filename:                    'main.js',
      js_filename_minified:           'main.min.js',
      js_vendor_filename:             'vendors.js',
      js_vendor_filename_minified:    'vendors.min.js',
      js_master_filename:             'scripts.js',
      js_master_filename_minified:    'scripts.min.js'
    },

    deploy: {
      folder:                 '../../../../demo',
    }
  };

  // various config files
  var stylelintConfig = grunt.file.readJSON('scss/.stylelintrc'),
      autoprefixConfig = { browsers: 'last 2 versions' };






  // Project configuration.
  grunt.initConfig({

    pkg: grunt.file.readJSON('package.json'),

    project: project,

    banner: '/*!\n' +
        ' * <%= pkg.name %> v<%= pkg.version %> (<%= pkg.homepage %>)\n' +
        ' */\n',





    // HTML
    // ----------------------------------------
    // 1. compile
    jade: {
      options: {
        compileDebug: false,
        pretty: true,
      },
      build: {
        files: [
          {
            expand: true,
            cwd: '<%= project.jade_dir %>',
            src: [
              '*.jade'
            ],
            dest: '<%= project.output.folder %>',
            ext: '.html',
            flatten: true
          }
        ]
      },
      deploy: {
        files: [
          {
            expand: true,
            cwd: '<%= project.jade_dir %>',
            src: [
              '*.jade'
            ],
            dest: '<%= project.output.html_folder %>',
            ext: '.html',
            flatten: true
          }
        ]
      }
    },





    // CSS
    // ----------------------------------------
    // 1. build
    sass: {
      build: {
        options: {
          sourceMap: true
        },
        files: {
          '<%= project.output.folder %><%= project.output.css_folder %><%= project.output.css_filename %>':
            '<%= project.sass_dir %><%= project.sass_filename %>'
        }
      },
      deploy: {
        files: {
          '<%= project.output.folder %><%= project.output.css_folder %><%= project.output.css_filename_minified %>':
            '<%= project.sass_dir %><%= project.sass_filename %>'
        }
      }
    },

    // 2. postcss
    //  a) lint the styles
    //  b) autoprefix
    //  c) minify (only for deploy command)
    postcss: {
      build: {
        options: {
          map: true,
          processors: [
            require('stylelint')(),
            require('autoprefixer')(autoprefixConfig)
          ]
        },
        src: '<%= project.output.folder %><%= project.output.css_folder %><%= project.output.css_filename %>'
      },
      deploy: {
        options: {
          map: false,
          processors: [
            require('stylelint')(),
            require('autoprefixer')(autoprefixConfig),
            require('cssnano')()
          ]
        },
        src: '<%= project.output.folder %><%= project.output.css_folder %><%= project.output.css_filename_minified %>'
      }
    },





    // JS
    // ----------------------------------------
    // 1. concat
    concat: {
      vendors: {
        src: '<%= project.js_vendor_files %>',
        dest: '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_vendor_filename %>'
      },
      build: {
        options: {
          sourceMap: true
        },
        src: '<%= project.js_files %>',
        dest: '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_filename %>'
      }
    },

    // 2. minify
    uglify: {
      vendors: {
        files: {
          '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_vendor_filename_minified %>': [
            '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_vendor_filename %>'
          ]
        }
      },
      build: {
        files: {
          '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_filename_minified %>': [
            '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_filename %>'
          ]
        }
      }
    },





    // Utils
    // ----------------------------------------
    // 1. copy files - only used for deployment
    copy: {
      css: {
        files : [{
          expand: true,
          src: [
            '<%= project.output.folder %><%= project.output.css_folder %><%= project.output.css_filename %>',
            '<%= project.output.folder %><%= project.output.css_folder %><%= project.output.css_filename_minified %>'
          ],
          dest: '<%= project.deploy.folder %>'
        }]
      },
      images: {
        files : [{
          expand: true,
          src: ['<%= project.images_dir %>**'],
          dest: '<%= project.deploy.folder %>'
        }]
      },
      html: {
        files : [{
          expand: true,
          src: ['<%= project.output.folder %>*.html'],
          dest: '<%= project.deploy.folder %>'
        }]
      },
      js: {
        files : [{
          expand: true,
          src: [
            // custom scripts
            '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_filename %>',
            // vendor scripts
            '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_vendor_filename %>',
            // minified
            '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_filename_minified %>',
            '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_vendor_filename_minified %>',
          ],
          dest: '<%= project.deploy.folder %>'
        }]
      },
      misc: {
        files : [{
          expand: true,
          src: ['<%= project.misc_dir %>**'],
          dest: '<%= project.deploy.folder %>'
        }]
      },
    },

    // 2. banners
    usebanner: {
      options: {
        position: 'top',
        banner: '<%= banner %>'
      },
      build: {
        src: [
          '<%= project.output.folder %><%= project.output.css_folder %><%= project.output.css_filename %>',
          '<%= project.output.folder %><%= project.output.css_folder %><%= project.output.css_filename_minified %>',
          '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_filename %>',
          '<%= project.output.folder %><%= project.output.js_folder %><%= project.output.js_filename_minified %>'
        ]
      }
    },

    // watch file changes
    watch: {
      sass: {
        files: ['<%= project.sass_dir %>*.scss','<%= project.sass_dir %>**/*.scss'],
        tasks: ['sass:build', 'postcss:build']
      },
      jade: {
        files: [ '<%= project.jade_dir %>*.jade', '<%= project.jade_dir %>**/*.jade'],
        tasks: ['jade:build']
      },
      js: {
        files: '<%= concat.build.src %>',
        tasks: ['concat:build']
      },
    }

  });



  // Load the plugins
  // ===================================
  require('load-grunt-tasks')(grunt, { scope: 'devDependencies' });
  require('time-grunt')(grunt);



  // Default task(s)
  // ===================================
  grunt.registerTask('default', ['deploy', 'watch']);
  // ----------------------------------------
  grunt.registerTask('deploy', function() {
    // build -> minify -> add our tag
    grunt.task.run([
      'build',
      'minify',
      'usebanner'
    ]);
  });

  grunt.registerTask('build', function() {
    grunt.task.run([
      // build html
      'jade',
      // build css
      'sass:build',
      'postcss:build',
      // build js
      'concat:vendors',
      'concat:build',
    ]);
  });

  grunt.registerTask('minify', function() {
    grunt.task.run([
      // minify css
      'sass:deploy',
      'postcss:deploy',
      // minify js
      'uglify',
    ]);
  });

  grunt.registerTask('export', function() {

    var target = grunt.option('target');
    if (target) {
      // adjust our project settings
      var new_settings = project;
        new_settings.deploy.folder = target;
      grunt.config.set('project', new_settings);
    }

    // build + output to a directory
    // default: ../../../demo
    grunt.task.run([
      'deploy',
      'copy',
    ]);
  });


  // quick tasks:
  // ----------------------------------------
  // build all css
  grunt.registerTask('css', ['sass', 'postcss']);
  // build all js
  grunt.registerTask('js', ['concat', 'uglify']);

};
