import json
from api import scoresync_pb2


def compare_leaderboards(old_leaderboard, new_leaderboard):
    rank_changes = []
    old_ranks = {entry["model"]: entry["rank"] for entry in old_leaderboard}
    new_ranks = {entry["model"]: entry["rank"] for entry in new_leaderboard}
    for entry in new_leaderboard:
        model_name = entry["model"]
        new_rank = new_ranks.get(model_name, None)
        old_rank = old_ranks.get(model_name, None)
        if old_rank is None:
            entry["is_new"] = True
            entry["rank_change"] = "same"
        elif new_rank < old_rank:
            entry["rank_change"] = "down"
        elif new_rank > old_rank:
            entry["rank_change"] = "up"
        else:
            entry["rank_change"] = "same"

        rank_changes.append(entry)

    return rank_changes


def AddDetails(self, request, context):

    with open(request.input_json_path) as f:
        data = json.load(f)

    leaderboard = data["leaderboard"]

    with open(request.old_json_path) as f:
        old_data = json.load(f)

    old_leaderboard = old_data["leaderboard"]

    with open("models_metadata.json") as f:
        model_details = json.load(f)

    meta_leaderboard = []
    for entry in leaderboard:
        model_name = entry["model"]
        model_info = model_details.get(model_name, {})

        entry["url"] = model_info.get("url", "N/A")
        entry["contribute"] = model_info.get(
            "contribute", model_info.get("contribute", "N/A")
        )
        entry["base_model"] = model_info.get("base_model", "N/A")
        entry["registr"] = model_info.get("registr", "N/A")
        meta_leaderboard.append(entry)

        meta_leaderboard = compare_leaderboards(old_leaderboard, meta_leaderboard)

    data["leaderboard"] = meta_leaderboard

    with open(request.output_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return scoresync_pb2.AddDetailsResponse()
