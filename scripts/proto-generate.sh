#!/bin/bash

pip install grpcio grpcio-tools

# SERVER

rm -rf ./server/sample_app/*pb2*.py
rm -rf ./server/chief_of_state/*pb2*.py

python -m grpc_tools.protoc \
    -I./proto/ \
    --python_out=./server/ \
    --grpc_python_out=./server/ \
    ./proto/sample_app/*.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./server/ \
    --grpc_python_out=./server/ \
    ./submodules/chief-of-state-protos/chief_of_state/writeside.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./server/ \
    --grpc_python_out=./server/ \
    ./submodules/chief-of-state-protos/chief_of_state/common.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./server/ \
    --grpc_python_out=./server/ \
    ./submodules/chief-of-state-protos/chief_of_state/service.proto


# CLIENT

rm -rf ./client/sample_app/
rm -rf ./client/chief_of_state/

python -m grpc_tools.protoc \
    -I./proto/ \
    --python_out=./client/ \
    --grpc_python_out=./client/ \
    ./proto/sample_app/*.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./client/ \
    --grpc_python_out=./client/ \
    ./submodules/chief-of-state-protos/chief_of_state/writeside.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./client/ \
    --grpc_python_out=./client/ \
    ./submodules/chief-of-state-protos/chief_of_state/common.proto

python -m grpc_tools.protoc \
    -I./submodules/chief-of-state-protos/ \
    --python_out=./client/ \
    --grpc_python_out=./client/ \
    ./submodules/chief-of-state-protos/chief_of_state/service.proto
