# # 找到gRPC插件
# GRPC_CPP_PLUGIN_PATH=`which grpc_cpp_plugin`

# # 生成gRPC代码
# protoc -I . --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=$GRPC_CPP_PLUGIN_PATH boolean_service.proto

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. algorithm.proto