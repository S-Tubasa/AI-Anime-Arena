import warnings

warnings.filterwarnings(
    "ignore", message="Protobuf gencode version.*is older than the runtime version.*"
)

import argparse
import grpc
from api import scoresync_pb2
from api import scoresync_pb2_grpc


def run(api, input_json_path, output_json_path, old_json_path):
    # Connect to the server
    with grpc.insecure_channel("localhost:9300") as channel:
        stub = scoresync_pb2_grpc.ScoreSyncServiceStub(channel)

        if api == "MakeRank":
            request = scoresync_pb2.MakeRankRequest(
                input_json_path=input_json_path, output_json_path=output_json_path
            )

            try:
                response = stub.MakeRank(request)
            except grpc.RpcError as e:
                print(f"gRPC call failed: {e.details()}")
                print(f"Status code: {e.code()}")

        if api == "CleanData":
            request = scoresync_pb2.CleanDataRequest(
                input_json_path=input_json_path, output_json_path=output_json_path
            )

            try:
                response = stub.CleanData(request)
            except grpc.RpcError as e:
                print(f"gRPC call failed: {e.details()}")
                print(f"Status code: {e.code()}")
        if api == "AddDetails":
            request = scoresync_pb2.AddDetailsRequest(
                input_json_path=input_json_path,
                output_json_path=output_json_path,
                old_json_path=old_json_path,
            )

            try:
                response = stub.AddDetails(request)
            except grpc.RpcError as e:
                print(f"gRPC call failed: {e.details()}")
                print(f"Status code: {e.code()}")

        if api == "MergeData":
            request = scoresync_pb2.MergeDataRequest(
                input_json_path=input_json_path, all_json_path=output_json_path
            )

            try:
                response = stub.MergeData(request)
            except grpc.RpcError as e:
                print(f"gRPC call failed: {e.details()}")
                print(f"Status code: {e.code()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON paths for gRPC request.")
    parser.add_argument("-a", "--api", required=True, help="The gRPC method to call.")
    parser.add_argument("-i", "--input_json_path", help="Path to the input JSON file.")
    parser.add_argument(
        "-o", "--output_json_path", help="Path to the output JSON file."
    )
    parser.add_argument("-d", "--old_json_path", help="Path to the old JSON file.")

    args = parser.parse_args()

    run(args.api, args.input_json_path, args.output_json_path, args.old_json_path)
