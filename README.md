[![Build Status](https://travis-ci.org/hhroc/yellr-server.svg)](https://travis-ci.org/hhroc/yellr-server)


Chat about yellr-server on Gitter! [Chat Now](https://gitter.im/hhroc/yellr-server)

# Yellr Server

[![Join the chat at https://gitter.im/hhroc/yellr-server](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/hhroc/yellr-server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is the server and admin component of the Yellr application

Setting up the moderator dev environment.
------

To make our moderator site you must have [npm](https://www.npmjs.com/),
[bower](http://bower.io/), [grunt](http://gruntjs.com/), and [ruby](https://www.ruby-lang.org/en/) (for SASS compilation),
installed.

Ubuntu:

    sudo apt-get update
    sudo apt-get install nodejs
    sudo apt-get install npm
    wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.23.2/install.sh | bash
    nvm install v0.10.24
    nvm use v0.10.24
    npm install bower
    npm install grunt
    sudo apt-get install ruby

Once the you have all of those, simply run `make` to compile all of the
frontend dependencies and if you’re going to do development, run `make dev`
to have grunt also watch all of your javascript and SASS files for changes.

    git clone https://github.com/hhroc/yellr-server
    cd yellr-server
    make clean
    make
    make dev

Getting server configured
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


Running the server
---------------

Once you have done everything above, you can run the server with the following

    cd yellr-server
    cd yellr-serv
    pserve developmentini
    
And that's it!
