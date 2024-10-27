# ref: https://github.com/lm-sys/FastChat/blob/main/fastchat/serve/monitor/deduplication.py
import pandas as pd
import numpy as np
from tqdm import tqdm
import logging


def deduplicate(df, percentile=0.9999):

    df["post_process_conv"] = df["prompt"].apply(lambda x: x[:10000])
    prompt_counts = df["post_process_conv"].value_counts()
    top_prompts = prompt_counts.head(20)
    # print(top_prompts)

    percentile_cutoff = prompt_counts.quantile(percentile)
    logging.info(f"{percentile*100} percentile count: {percentile_cutoff}")

    high_frequency_prompts = prompt_counts[prompt_counts > percentile_cutoff].index
    logging.info(
        f"Number of high frequency prompts: {len(high_frequency_prompts)}/{len(prompt_counts)}"
    )

    dedup_tags = np.array(
        [{"high_freq": False, "sampled": True} for _ in range(len(df))]
    )
    high_freq_groups = df.groupby("post_process_conv")
    for prompt in tqdm(high_frequency_prompts):
        df_high_freq = high_freq_groups.get_group(prompt)
        sampled_indices = df_high_freq.sample(n=int(percentile_cutoff)).index
        dedup_tags[df_high_freq.index] = {"high_freq": True, "sampled": False}
        dedup_tags[sampled_indices] = {"high_freq": True, "sampled": True}

    df["dedup_tag"] = dedup_tags

    df = df.drop(columns=["post_process_conv"])

    return df
