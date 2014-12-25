all: clean dependencies compile

dependencies:
	npm install
	bower install

compile:
	grunt compile

clean:
	rm -rf assets/js/
	rm -rf assets/css/

dev: clean dependencies
	grunt
