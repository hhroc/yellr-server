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
                    'yellr-serv/yellrserv/moderator/assets/js/scripts.js' : [
                        'bower_components/cryptojslib/rollups/hmac-sha256.js',
                        'bower_components/jquery/dist/jquery.js',
                        'bower_components/angular/angular.js',
                        'bower_components/angular-ui-router/release/angular-ui-router.js',
                        'bower_components/angular-mocks/angular-mocks.js',
                        'bower_components/angular-foundation/mm-foundation.js',
                        'bower_components/angular-foundation/mm-foundation-tpls.js',
                        'app/*.js', // root files first
                        'app/**/*.js', // then everything else
                        '!app/tests/**/*.js' // ignore tests
                    ]
                },
            }
        },

        uglify: {
            options : {
                sourceMap : true,
                sourceMapIncludeSources : true,
                sourceMapIn : 'yellr-serv/yellrserv/moderator/assets/js/scripts.js.map',
                sourceMapName: 'yellr-serv/yellrserv/moderator/assets/js/scripts.min.js.map'
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
                tasks: ['concat_sourcemap', 'uglify', 'clean'],
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
            },
            js: {
                files: [{
                    src: [
                        'app/*.js',
                        'app/**/*.js'
                    ],
                    dest: 'yellr-serv/yellrserv/moderator/assets/js/'
                }],
                verbose: true,
                flatten: true
            }
        },

        clean: {
            js: ['yellr-serv/yellrserv/moderator/assets/js/scripts.js', 'yellr-serv/yellrserv/moderator/assets/js/scripts.js.map', 'moderator/'],
        }
    });

    grunt.loadNpmTasks('grunt-concat-sourcemap');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-sync');

    grunt.registerTask('default', ['concat_sourcemap', 'uglify', 'sync', 'sass', 'watch']);
    grunt.registerTask('compile', ['concat_sourcemap', 'uglify', 'sync', 'sass']);
};
