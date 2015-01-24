[![Build Status](https://travis-ci.org/hhroc/yellr-server.svg)](https://travis-ci.org/hhroc/yellr-server)
# Yellr Server

This is the server and admin component of the Yellr application

Setting up the moderator dev environment.
------

To make our moderator site you must have [npm](https://www.npmjs.com/),
[bower](http://bower.io/), [grunt](http://gruntjs.com/), and [ruby](https://www.ruby-lang.org/en/) (for SASS compilation),
installed.

Once the you have all of those, simply run `make` to compile all of the
frontend dependencies and if you’re going to do development, run `make dev`
to have grunt also watch all of your javascript and SASS files for changes.

Getting server Started
---------------

Prior to getting your server started make sure you setup your own virtual
environment and then run these commands.

    cd yellr-serv/
    $VENV/bin/python setup.py develop
    $VENV/bin/initialize_yellr-serv_db development.ini
    

You will also need to install the ImageMagick tools.

####Ubuntu:

    sudo apt-get install imagemagick

####Fedora:

    sudo yum install imagemagick

####Windows:

go here for instructions: http://www.imagemagick.org/script/binary-releases.php#windows


Once imagemagick is installed, and you have configured you environment, you can run the development server:

    $VENV/bin/pserve development.ini


