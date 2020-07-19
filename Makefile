DCO := docker-compose --project-directory . -f ./docker/docker-compose.yml

.phony: setup
setup:
	git submodule update --init

.phony: protogen
protogen:
	@docker run \
		-v `pwd`:/mnt/local/ \
		-w /mnt/local/ \
		python:3.7.6-stretch \
		./scripts/proto-generate.sh

.phony: shell
shell:
	@docker run -it \
		-v `pwd`:/mnt/local/ \
		-w /mnt/local/ \
		python:3.7.6-stretch \
		bash


.phony: test-shell
test-shell:
	@docker run -it \
		-v `pwd`:/mnt/local/ \
		-w /mnt/local/server \
		-p 9090:9090 \
		cos-python-sample:latest \
		bash

.phony: dco
dco:
	@echo $(DCO)

.phony: ps
ps:
	@ $(DCO) ps

.phony: logs
logs:
	@ $(DCO) logs -f --tail="all"

.phony: build
build:
	@ $(DCO) build

.phony: up
up:
	@ $(DCO) up -d

.phony: down
down:
	@ $(DCO) down -t 0 --remove-orphans
