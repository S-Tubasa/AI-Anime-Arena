import logging
import grpc
from api import scoresync_pb2_grpc
from .makerank import MakeRank
from .cleandata import CleanData
from .add_details import AddDetails
from .mergedata import MergeData


class ScoreSync(scoresync_pb2_grpc.ScoreSyncServiceServicer):
    pass


# ここにメゾッドを追加
ScoreSync.MakeRank = MakeRank
ScoreSync.CleanData = CleanData
ScoreSync.AddDetails = AddDetails
ScoreSync.MergeData = MergeData


class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        method_name = handler_call_details.method
        logging.info(f"gRPC method called: {method_name}")

        handler = continuation(handler_call_details)

        if handler is None:
            return None

        def log_request(request, context):
            logging.info(f"Request:{str(request).replace('\n', '').rstrip()}")
            response = handler.unary_unary(request, context)
            logging.info(f"Response: {str(request).replace('\n', '').rstrip()}")
            return response

        return grpc.unary_unary_rpc_method_handler(
            log_request,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )
