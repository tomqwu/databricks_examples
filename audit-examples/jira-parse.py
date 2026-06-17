import pandas as pd

# Pull columns A:E with the header row
df = xl("A:E", headers=True)
df = df.dropna(how="all").reset_index(drop=True)

# Parse Load Date (col A) so "latest" compares as real dates, not text
df["_load"] = pd.to_datetime(df.iloc[:, 0], errors="coerce").fillna(pd.Timestamp("1900-01-01"))

# Key = Context (col D) + Name (col E)
df["_key"] = (df.iloc[:, 3].astype(str).str.strip() + " || "
              + df.iloc[:, 4].astype(str).str.strip())

# For each key, keep the row with the latest Load Date
idx = df.groupby("_key")["_load"].idxmax()

# Output A:E only, in original order
out = df.loc[idx].sort_index().iloc[:, 0:5].reset_index(drop=True)
out