# =====================================================================
# Python in Excel version - paste everything below the line into a
# =PY( ) cell  (Formulas > Insert Python, or type =PY and press Tab)
#
#  1. Save the Jira export as .xlsx first (csv can't keep the formula).
#  2. Put the formula in an empty cell clear of the data - e.g. two
#     columns right of the export on row 1, or on a new sheet - so the
#     result table has room to spill.
#  3. Adjust the xl() range to cover the whole export (click-selecting
#     the range while the PY editor is open inserts it for you).
#  4. Set the cell output to "Excel Values": right-click the cell >
#     Python Output > Excel Values (or the PY menu by the formula bar).
#
#  Handles all three duplicate-header cases: literal repeated
#  "Attachment" headers, pandas-style "Attachment.1", and Excel-Table
#  renames "Attachment2" - attachment cells are read by position.
# =====================================================================

import pandas as pd
import re

df = xl("A1:T2000", headers=True)     # <- adjust to the export range

KEEP = ["Issue key", "Custom field (MAL Code)", "Custom field (Action)",
        "Custom field (Additional Information)", "Updated"]
ATT = re.compile(r"(?i)^attachment[\s.]*\d*$")   # Attachment / Attachment.1 / Attachment2
HIT = re.compile(r"(?i)AKCLDAC-\d+.*\.xlsx$")    # which filenames count

cols = list(df.columns)
missing = [k for k in KEEP if k not in cols]
if missing:
    raise ValueError(f"Export missing columns: {missing}")
att_idx = [i for i, c in enumerate(cols) if ATT.match(str(c).strip())]

rows = []
for _, r in df.iterrows():
    for i in att_idx:
        cell = r.iloc[i]
        if not isinstance(cell, str) or not cell.strip():
            continue
        for entry in cell.splitlines():
            parts = entry.split(";", 3)          # date ; uploader ; filename ; url
            if len(parts) < 3:
                continue
            name = parts[2].strip()
            if HIT.search(name):
                date = parts[0].strip().split(" ")[0].replace("/", "-")  # 10/Apr/26 -> 10-Apr-26
                rows.append([r["Issue key"], name, date] + [r[k] for k in KEEP[1:]])

pd.DataFrame(rows, columns=["Issue key", "Xls", "Date"] + KEEP[1:])