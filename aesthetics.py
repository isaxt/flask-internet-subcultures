from pathlib import Path

import numpy as np
import pandas as pd

DATA_FILE = Path(__file__).parent / "data" / "train-00000-of-00001.parquet"

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Put the parquet file at {DATA_FILE} (download it from the Hugging Face dataset page)."
    )

# Load once when the app starts, not on every page view.
df = pd.read_parquet(DATA_FILE)
df = df.dropna(subset=["title", "overview"])
df = df[df["overview"].str.strip() != ""].reset_index(drop=True)


def as_list(value, limit=5):
    """List columns can be None or numpy arrays; return a plain short list."""
    if not isinstance(value, (list, tuple, np.ndarray)):
        return []  # None or NaN
    return [str(v) for v in list(value)[:limit]]


def short(text, n=320):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "..."


def get_pair():
    """Return two random aesthetics as small dictionaries for the template."""
    rows = df.sample(2)
    return [
        {
            "title": row["title"],
            "overview": short(row["overview"]),
            "colours": as_list(row["key_colours"]),
            "motifs": as_list(row["key_motifs"]),
            "decade": row["extract_decade"] if isinstance(row["extract_decade"], str) else "",
        }
        for _, row in rows.iterrows()
    ]
