from api import scoresync_pb2
import pandas as pd
import json
import logging


def MergeData(self, request, context):

    with open(request.input_json_path, "r", encoding="utf-8") as f:
        data_inpt = json.load(f)
    df_inpt = pd.json_normalize(data_inpt)

    with open(request.all_json_path, "r", encoding="utf-8") as f:
        data_all = json.load(f)
    df_all = pd.json_normalize(data_all)

    df_merged = pd.concat([df_all, df_inpt], ignore_index=True)

    df_merged.to_json(
        request.all_json_path,
        orient="records",
        indent=4,
        force_ascii=False,
    )

    return scoresync_pb2.MergeDataResponse()
