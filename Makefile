all: dependencies compile

dependencies:
	npm install
	./node_modules/bower/bin/bower install

compile:
	mkdir -p app/sass/deps
	mkdir -p assets/templates
	cp -a bower_components/foundation/scss/. app/sass/deps/
	ls
	ls app/sass/
	ls app/sass/deps/
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
