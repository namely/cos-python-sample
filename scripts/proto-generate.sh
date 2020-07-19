#!/bin/bash

pip install grpcio grpcio-tools

rm -rf ./server/app/*pb2*.py
rm -rf ./server/chief_of_state/*pb2*.py

python -m grpc_tools.protoc \
    -I./proto/ \
    --python_out=./server/ \
    --grpc_python_out=./server/ \
    ./proto/app/*.proto

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
