import warnings

warnings.filterwarnings(
    "ignore", message="Protobuf gencode version.*is older than the runtime version.*"
)

from concurrent import futures
import logging
import grpc
from grpc_reflection.v1alpha import reflection
from api import scoresync_pb2
from api import scoresync_pb2_grpc
import argparse
from services.server import LoggingInterceptor, ScoreSync


def serve(port=9300, log_to_console=False):
    if log_to_console:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    else:
        logging.basicConfig(
            filename="/log/scoresync/server.log",
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
        )

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LoggingInterceptor()],  # インターセプターを追加
    )

    scoresync_pb2_grpc.add_ScoreSyncServiceServicer_to_server(ScoreSync(), server)

    SERVICE_NAMES = (
        scoresync_pb2.DESCRIPTOR.services_by_name["ScoreSyncService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info(f"Server started, listening on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gRPC Server")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Log to console instead of file"
    )
    args = parser.parse_args()

    log_to_console = args.debug
    serve(log_to_console=log_to_console)
