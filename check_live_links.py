"""
check_live_links.py
-------------------
Removes dead URLs from dataset.csv and writes a cleaned file.

WHY RUN THIS LOCALLY:
A live-link check needs real internet access to each website. Run it on your
own computer (not inside a restricted environment).

USAGE:
    pip install pandas requests
    python check_live_links.py

INPUT : dataset.csv          (columns: url, label)
OUTPUT: dataset_live.csv      (only URLs that responded)
        dataset_dead.csv      (the ones removed, for your records)
"""

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_FILE  = "new_dataset_additions_candidates.csv"
LIVE_FILE   = "new_dataset_live.csv"
DEAD_FILE   = "new_dataset_dead.csv"
TIMEOUT     = 8          # seconds to wait per URL
MAX_WORKERS = 30         # how many URLs to check at once
HEADERS     = {"User-Agent": "Mozilla/5.0 (compatible; LinkChecker/1.0)"}


def is_live(url: str) -> bool:
    """Return True if the URL responds at all (even with an error page)."""
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url
    try:
        # allow_redirects follows the site if it moved; we only care that
        # *something* answered. A dead domain raises an exception instead.
        resp = requests.get(
            url, headers=HEADERS, timeout=TIMEOUT,
            allow_redirects=True, stream=True
        )
        # Treat "gone" responses as dead, everything else as live.
        return resp.status_code not in (404, 410)
    except requests.RequestException:
        return False


def main():
    df = pd.read_csv(INPUT_FILE)
    urls = df["url"].tolist()
    print(f"Checking {len(urls)} URLs (timeout {TIMEOUT}s, {MAX_WORKERS} at a time)...\n")

    results = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(is_live, u): u for u in urls}
        done = 0
        for fut in as_completed(futures):
            u = futures[fut]
            results[u] = fut.result()
            done += 1
            if done % 25 == 0 or done == len(urls):
                print(f"  checked {done}/{len(urls)}")

    df["is_live"] = df["url"].map(results)
    live = df[df["is_live"]].drop(columns="is_live")
    dead = df[~df["is_live"]].drop(columns="is_live")

    live.to_csv(LIVE_FILE, index=False)
    dead.to_csv(DEAD_FILE, index=False)

    print("\n--- Summary ---")
    print(f"Live URLs kept   : {len(live)}  ->  {LIVE_FILE}")
    print(f"Dead URLs removed: {len(dead)}  ->  {DEAD_FILE}")
    print("\nLive label balance:")
    print(live["label"].value_counts().rename({0: "Legitimate", 1: "Fraudulent"}))
    print("\nTip: if removing dead links unbalanced the classes, downsample the")
    print("larger class so both have equal counts before training.")


if __name__ == "__main__":
    main()
