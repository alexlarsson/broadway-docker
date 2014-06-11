all: image run

image:
	docker build -t broadway-repo .

run:
	docker run -d -p 9999:80 broadway-repo
