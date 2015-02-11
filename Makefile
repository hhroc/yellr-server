all: dependencies compile

dependencies:
	npm install
	./node_modules/bower/bin/bower install

compile:
	# Make dirs for static assets
	mkdir -p app/sass/deps
	mkdir -p assets/templates
	mkdir -p yellr-serv/yellrserv/moderator/assets/css
	mkdir -p yellr-serv/yellrserv/moderator/assets/css/deps
	mkdir -p yellr-serv/yellrserv/moderator/assets/js
	mkdir -p yellr-serv/yellrserv/moderator/epiceditor
	mkdir -p yellr-serv/yellrserv/moderator/epiceditor/themes
	# Copy Foundation
	cp -a bower_components/foundation/scss/. app/sass/deps/
	cp -a bower_components/foundation-datepicker/stylesheets/foundation-datepicker.css yellr-serv/yellrserv/moderator/assets/css/deps/_foundation-datepicker.css
	# Copy Bourbon
	cp -a bower_components/bourbon/app/assets/stylesheets/. app/sass/deps/
	# Copy ng-tags-input css
	cp bower_components/ng-tags-input/ng-tags-input.min.css yellr-serv/yellrserv/moderator/assets/css/ng-tags-input.min.css
	# Copy Leaflet things
	cp bower_components/leaflet/dist/leaflet.css yellr-serv/yellrserv/moderator/assets/css/leaflet.css
	cp -a bower_components/leaflet/dist/images/. yellr-serv/yellrserv/moderator/assets/css/images
	# Copy EpicEditor Themes
	cp -a bower_components/epiceditor/epiceditor/themes/. yellr-serv/yellrserv/moderator/epiceditor/themes/
	# Copy ZeroClipboard .swf
	cp bower_components/zeroclipboard/dist/ZeroClipboard.swf yellr-serv/yellrserv/moderator/assets/js/ZeroClipboard.swf
	# Compile
	./node_modules/grunt-cli/bin/grunt compile

clean:
	rm -rf yellr-serv/yellrserv/moderator/assets/js/
	rm -rf yellr-serv/yellrserv/moderator/assets/css/
	rm -rf yellr-serv/yellrserv/moderator/assets/templates/
	rm -rf yellrserv/yellrserv/moderator/epiceditor/
	rm -rf bower_components
	rm -rf node_modules
	rm -rf app/sass/deps/

dev: clean dependencies compile
	./node_modules/grunt-cli/bin/grunt watch

test:
	./node_modules/karma/bin/karma start --browsers Firefox --single-run
	./node_modules/jshint/bin/jshint app/**/*.js
