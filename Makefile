all: clean dependencies compile

dependencies:
	npm install
	bower install

compile:
	mkdir -p app/sass/deps
	mkdir -p assets/templates
	cp -r bower_components/foundation/scss/ app/sass/deps/
	cp -r app/templates/ assets/templates/
	grunt compile

clean:
	rm -rf assets/js/
	rm -rf assets/css/
	rm -rf app/sass/deps/

dev: clean dependencies compile
	grunt watch
