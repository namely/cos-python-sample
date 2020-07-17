

.phony: shell
shell:
	docker run -it \
		-v `pwd`:/mnt/local/ \
		-w /mnt/local/ \
		-p 50051:50051 \
		python:3.7.6-stretch \
		bash

.phony: pip-install
pip-install:
	pip install -r requirements.txt


.phony: proto-gen
proto-gen:

	rm -rf ./app/*pb2*.py

	python -m grpc_tools.protoc \
		-I./proto/ \
		--python_out=. \
		--grpc_python_out=. \
		./proto/app/*.proto

	rm -rf ./handler/*pb2*.py

	python -m grpc_tools.protoc \
		-I./submodules/chief-of-state/protos/ \
		--python_out=./handler/ \
		--grpc_python_out=./handler/ \
		./submodules/chief-of-state/protos/chief_of_state/*write*_handler.proto




.phony: run-api
run-api:
	@python -m app
