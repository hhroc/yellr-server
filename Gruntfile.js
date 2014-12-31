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
                    'app/*.js', // root files first
                    'app/**/*.js' // then everything else
                ],
                dest: 'assets/js/scripts.js'
            }
        },

        uglify: {
            options : {
                sourceMap : true,
                sourceMapIncludeSources : true,
                sourceMapIn : 'assets/js/scripts.js.map'
            },
            dist: {
                src: 'assets/js/scripts.js',
                dest: 'assets/js/scripts.min.js'
            }
        },

        sass: {
            dist: {
                options: {
                    style: 'compress',
                },
                files: {
                    'assets/css/site.css': 'app/sass/site.scss'
                }
            }
        },

        watch: {
            js: {
                files: ['app/**/*.js'],
                tasks: ['concat_js', 'uglify_js', 'clean'],
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
            }
        },

        clean: {
            js: ['assets/js/scripts.js', 'assets/js/scripts.js.map'],
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-clean');

    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'clean', 'watch']);
    grunt.registerTask('compile', ['concat', 'uglify', 'sass', 'clean']);
};
