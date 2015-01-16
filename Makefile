all: dependencies compile

dependencies:
	npm install
	./node_modules/bower/bin/bower install

compile:
	# Make dirs for static assets
	mkdir -p app/sass/deps
	mkdir -p assets/templates
	mkdir -p yellr-serv/yellrserv/moderator/assets/css
	# Copy dependencies
	cp -a bower_components/foundation/scss/. app/sass/deps/
	cp -a bower_components/twbs-bootstrap-sass/assets/stylesheets/. app/sass/deps/
	cp bower_components/leaflet/dist/leaflet.css yellr-serv/yellrserv/moderator/assets/css/leaflet.css
	cp bower_components/leaflet-draw/dist/leaflet.draw.css yellr-serv/yellrserv/moderator/assets/css/leaflet-draw.css
	cp -a bower_components/leaflet-draw/dist/images/. yellr-serv/yellrserv/moderator/assets/css/images/
	cp bower_components/mapbox.js/mapbox.standalone.css yellr-serv/yellrserv/moderator/assets/css/mapbox.css
	cp -a bower_components/mapbox.js/images/. yellr-serv/yellrserv/moderator/assets/css/images/
	./node_modules/grunt-cli/bin/grunt compile

clean:
	rm -rf yellr-serv/yellrserv/moderator/assets/js/
	rm -rf yellr-serv/yellrserv/moderator/assets/css/
	rm -rf yellr-serv/yellrserv/moderator/assets/templates/
	rm -rf bower_components
	rm -rf node_modules
	rm -rf app/sass/deps/

dev: clean dependencies compile
	./node_modules/grunt-cli/bin/grunt watch

test:
	./node_modules/karma/bin/karma start --browsers Firefox --single-run
	./node_modules/jshint/bin/jshint app/**/*.js
