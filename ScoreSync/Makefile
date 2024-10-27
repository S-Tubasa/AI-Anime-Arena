PHONY: gen
gen:
	rm -fr ./api/*_pb2.py ./api/*_pb2_grpc.py ./api/*.pyi
	python -m grpc_tools.protoc \
		-I . \
		--python_out=. \
		--grpc_python_out=. \
		--plugin=protoc-gen-mypy=$$(which protoc-gen-mypy) \
		--mypy_out=. \
		./api/*.proto
