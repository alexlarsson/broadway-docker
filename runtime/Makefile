all: image

image: broadway.repo Dockerfile init.sh panel.js
	docker build -t broadway .

broadway.repo: broadway.repo.in
	sed "s/%%IP%%/`hostname -I | awk '{print $$1}'`/" broadway.repo.in > broadway.repo
