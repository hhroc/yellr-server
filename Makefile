all: clean dependencies compile

dependencies:
	npm install
	./node_modules/bower/bin/bower install

compile:
	mkdir -p app/sass/deps
	mkdir -p assets/templates
	cp -r bower_components/foundation/scss/ app/sass/deps/
	cp -r app/templates/ assets/templates/
	./node_modules/grunt-cli/bin/grunt compile

clean:
	rm -rf assets/js/
	rm -rf assets/css/
	rm -rf app/sass/deps/

dev: clean dependencies compile
	./node_modules/grunt-cli/bin/grunt watch
