import json
import pandas as pd
from api import scoresync_pb2
import logging
from .deduplication import deduplicate


def CleanData(self, request, context):

    with open(request.input_json_path) as f:
        data = json.load(f)
    df = pd.json_normalize(data)

    # 翻訳を使用している場合、翻訳されたプロンプトを使用
    df["prompt"] = df.apply(
        lambda row: (
            row["prompt.generated"]
            if row["prompt.translation"]
            else row["prompt.original"]
        ),
        axis=1,
    )
    logging.info(f"Loaded {len(df)} rows")
    df = deduplicate(df)

    df["translation"] = df["prompt.translation"]
    df = df.drop(
        columns=["prompt.original", "prompt.generated", "prompt.translation", "prompt"]
    )
    df = df.drop(columns=["process.task_b", "process.task_a"])
    df = df.drop(columns=["model_a_img", "model_b_img"])
    df = df.drop(columns=["judge"])

    logging.info(f"Cleand {len(df)} rows")

    df.to_json(
        request.output_json_path,
        orient="records",
        indent=4,
        force_ascii=False,
    )
    return scoresync_pb2.CleanDataResponse()
