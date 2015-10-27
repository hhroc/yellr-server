'use strict';

module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat_sourcemap: {
            options: {
                sourceRoot: '/moderator/assets/js/'
            },
            dist: {
                files: {
                    'server/yellr_server/moderator/assets/js/scripts.js': [
                        'bower_components/cryptojslib/rollups/hmac-sha256.js',
                        'bower_components/jquery/dist/jquery.js',
                        'bower_components/angular/angular.js',
                        'bower_components/zeroclipboard/dist/ZeroClipboard.js',
                        'bower_components/ng-clip/dest/ng-clip.min.js',
                        'bower_components/ng-tags-input/ng-tags-input.js',
                        'bower_components/leaflet/dist/leaflet.js',
                        'bower_components/epiceditor/epiceditor/js/epiceditor.js',
                        'bower_components/async/lib/async.js',
                        'bower_components/masonry/dist/masonry.pkgd.min.js',
                        'bower_components/angular-masonry/angular-masonry.js',
                        'bower_components/angular-ui-router/release/angular-ui-router.js',
                        'bower_components/angular-mocks/angular-mocks.js',
                        'bower_components/angular-foundation/mm-foundation-tpls.js',
                        'bower_components/foundation-datepicker/js/foundation-datepicker.js',
                        'app/*.js', // root files first
                        'app/**/*.js', // then everything else
                        '!app/tests/**/*.js' // ignore tests
                    ]
                }
            }
        },

        concat: {
            css: {
                src: [],
                dest: []
            }
        },

        uglify: {
            options: {
                sourceMap: true,
                sourceMapIncludeSources: true,
                sourceMapIn: 'server/yellr_server/moderator/assets/js/scripts.js.map',
                sourceMapName: 'server/yellr_server/moderator/assets/js/scripts.min.js.map'
            },
            dist: {
                src: 'server/yellr_server/moderator/assets/js/scripts.js',
                dest: 'server/yellr_server/moderator/assets/js/scripts.min.js'
            }
        },

        sass: {
            dist: {
                options: {
                    style: 'compress'
                },
                files: {
                    'server/yellr_server/moderator/assets/css/site.css': 'app/sass/site.scss'
                }
            }
        },

        watch: {
            js: {
                files: ['app/**/*.js'],
                tasks: ['concat_sourcemap', 'uglify', 'clean', 'sync:sourcemap', 'sync:js'],
                options: {
                    spawn: false
                }
            },
            sass: {
                files: ['app/sass/**/*.scss'],
                tasks: ['sass'],
                options: {
                    spawn: false
                }
            },
            html: {
                files: ['app/templates/**/*.html'],
                tasks: ['sync'],
                options: {
                    spawn: false
                }
            }
        },

        sync: {
            html: {
                files: [{
                    cwd: 'app/templates/',
                    src: [
                        '**/*.html'
                    ],
                    dest: 'server/yellr_server/moderator/assets/templates/'
                }],
                verbose: true,
                flatten: true
            },
            js: {
                files: [{
                    src: [
                        'app/*.js',
                        'app/**/*.js'
                    ],
                    dest: 'server/yellr_server/moderator/assets/js/'
                }],
                verbose: true,
                flatten: true
            },
            sourcemap: {
                files: [{
                    cwd: 'server/yellr_server/moderator/assets/js/',
                    src: [
                        'scripts.min.js.map'
                    ],
                    dest: 'server/yellr_server/moderator/'
                }],
                verbose: true,
                flatten: true
            }
        },

        clean: {
            js: ['server/yellr_server/moderator/assets/js/scripts.js', 'server/yellr_server/moderator/assets/js/scripts.js.map', 'moderator/']
        }
    });

    grunt.loadNpmTasks('grunt-concat-sourcemap');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-sync');

    grunt.registerTask('default', ['concat_sourcemap', 'uglify', 'sync', 'sass', 'watch']);
    grunt.registerTask('compile', ['concat_sourcemap', 'uglify', 'sync', 'sass']);
};
