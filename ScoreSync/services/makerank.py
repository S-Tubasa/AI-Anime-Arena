from api import scoresync_pb2
import pandas as pd
import json
import logging
import datetime
from .elo_analysis import compute_mle_elo, get_bootstrap_result


def generate_bootstrap_scores_json(df, wins_per_model):
    # 各モデルの下限値、中央値、上限値を計算
    bars = pd.DataFrame(
        {
            "model": df.columns,
            "lower": df.quantile(0.025),
            "rating": df.quantile(0.5),
            "upper": df.quantile(0.975),
        }
    )

    # スコアを整数に丸める
    bars["score"] = bars["rating"].round().astype(int)

    # 95%信頼区間を計算
    bars["ci_plus"] = (bars["upper"] - bars["rating"]).round().astype(int)
    bars["ci_minus"] = (bars["rating"] - bars["lower"]).round().astype(int)
    bars["95%_ci"] = (
        "+" + bars["ci_plus"].astype(str) + "/-" + bars["ci_minus"].astype(str)
    )

    # bars = bars.sort_values("rating", ascending=False)
    # bars["RANK"] = bars["rating"].rank(method="min", ascending=False).astype(int)
    bars = bars.sort_values("score", ascending=False)
    bars["rank"] = bars["score"].rank(method="min", ascending=False).astype(int)

    bars = bars.merge(
        wins_per_model.rename("vote"), left_on="model", right_index=True, how="left"
    )

    # 必要な列を選択
    leaderboard = bars[["rank", "model", "95%_ci", "score", "vote"]].to_dict(
        orient="records"
    )

    return leaderboard


def MakeRank(self, request, context):

    with open(request.input_json_path, "r") as file:
        battles = pd.read_json(file).sort_values(ascending=True, by=["tstamp"])

    battles = battles[battles["anony"] == True]
    battles = battles[battles["dedup_tag"].apply(lambda x: x.get("sampled", False))]

    logging.info(f"Loaded {len(battles)} battles")

    winning_models = pd.concat(
        [
            battles.loc[battles["winner"] == "model_a", "model_a"],
            battles.loc[battles["winner"] == "model_b", "model_b"],
        ]
    )
    wins_per_model = winning_models.value_counts()

    BOOTSTRAP_ROUNDS = 100

    bootstrap_elo_lu = get_bootstrap_result(battles, compute_mle_elo, BOOTSTRAP_ROUNDS)
    leaderboard = generate_bootstrap_scores_json(bootstrap_elo_lu, wins_per_model)

    # リーダーボードのメタデータを追加
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M")

    metadata = {
        "total_models": len(wins_per_model),
        "total_votes": len(battles),
        "last_updated": formatted_date,
    }

    json_result = {"metadata": metadata, "leaderboard": leaderboard}

    with open(request.output_json_path, "w", encoding="utf-8") as f:
        json.dump(json_result, f, ensure_ascii=False, indent=4)

    return scoresync_pb2.MakeRankResponse()
