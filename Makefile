

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
	rm -rf app/protobuf
	mkdir app/protobuf
	python -m grpc_tools.protoc \
		-I./proto/ \
		--python_out=. \
		--grpc_python_out=. \
		./proto/app/*.proto
