'use strict';

module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat: {
            options: {
                sourceMap :true
            },
            dist: {
                src: [
                    'bower_components/cryptojslib/rollups/hmac-sha256.js',
                    'bower_components/angular/angular.js',
                    'bower_components/angular-ui-router/release/angular-ui-router.js',
                    'bower_components/angular-mocks/angular-mocks.js',
                    'app/*.js', // root files first
                    'app/**/*.js', // then everything else
                    '!app/tests/**/*.js' // ignore tests
                ],
                dest: 'yellr-serv/yellrserv/moderator/assets/js/scripts.js'
            }
        },

        uglify: {
            options : {
                sourceMap : true,
                sourceMapIncludeSources : true,
                sourceMapIn : 'yellr-serv/yellrserv/moderator/assets/js/scripts.js.map'
            },
            dist: {
                src: 'yellr-serv/yellrserv/moderator/assets/js/scripts.js',
                dest: 'yellr-serv/yellrserv/moderator/assets/js/scripts.min.js'
            }
        },

        sass: {
            dist: {
                options: {
                    style: 'compress',
                },
                files: {
                    'yellr-serv/yellrserv/moderator/assets/css/site.css': 'app/sass/site.scss'
                }
            }
        },

        watch: {
            js: {
                files: ['app/**/*.js'],
                tasks: ['concat', 'uglify', 'clean'],
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
                    dest: 'yellr-serv/yellrserv/moderator/assets/templates/',
                }],
                verbose: true,
                flatten: true
            }
        },

        clean: {
            js: ['yellr-serv/yellrserv/moderator/assets/js/scripts.js', 'yellr-serv/yellrserv/moderator/assets/js/scripts.js.map'],
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-sync');

    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'clean', 'sync', 'watch']);
    grunt.registerTask('compile', ['concat', 'uglify', 'sass', 'clean', 'sync']);
};
