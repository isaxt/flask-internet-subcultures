# %% Run these cells in VS Code (Jupyter extension) to look at the data before/after building.
import pandas as pd
df = pd.read_parquet("data/train-00000-of-00001.parquet")
df.shape, df.dtypes

# %%
df.isna().sum()

# %%
df["extract_decade"].value_counts().head(10)

# %%
df[["title", "overview", "key_motifs", "key_colours"]].sample(5)
