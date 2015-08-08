[![Build Status](https://travis-ci.org/hhroc/yellr-server.svg)](https://travis-ci.org/hhroc/yellr-server)


Chat about yellr-server on Gitter! [Chat Now](https://gitter.im/hhroc/yellr-server)

# Yellr Server

[![Join the chat at https://gitter.im/hhroc/yellr-server](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/hhroc/yellr-server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is the server and admin component of the Yellr application

Setting up the moderator dev environment.
------

To make our moderator site you must have [npm](https://www.npmjs.com/),
[bower](http://bower.io/), [grunt](http://gruntjs.com/), and [ruby](https://www.ruby-lang.org/en/) (for SASS compilation),
installed. These instructions assume that you’re using bash.

Ubuntu:

```bash
    sudo apt-get update
    # This installs [nvm](https://github.com/creationix/nvm) which is a node version manager
    wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.23.2/install.sh | bash
    # installs v0.10.24 of node
    nvm install v0.10.24
    nvm use v0.10.24
    # installs bower and grunt which is used for javascript make
    npm install -g bower
    npm install -g grunt-cli
    # ruby is used for sass compilation
    sudo apt-get install ruby
    sudo gem install sass
```

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
    sqlite3 yellr-serv.sqlite < ./zipcodes/insert_zips_sqlite.sql
    
Note: there is a seperate zipcode sql file for production (postgresql server) called insert_zips.sql.
    
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
