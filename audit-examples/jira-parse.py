# =====================================================================
# Python in Excel - v2
# Replace the whole contents of the =PY( ) cell with everything below.
#
# Changes vs v1:
#   - Likely cause of your error: the range stopped at column T and the
#     custom-field / Attachment columns sit further right. Widen the
#     xl() range to cover ALL columns of the export.
#   - Header matching is now tolerant (case, extra/non-breaking spaces,
#     "MAL Code" vs "Custom field (MAL Code)" variants).
#   - If anything is still missing, instead of an error dialog it spills
#     a Diagnostic column listing the real headers found in the range -
#     read it off the sheet and we adjust KEEP to match.
# =====================================================================

import pandas as pd
import re

df = xl("'JIRA 2026-06-10T14_09_00-0400'!A1:CZ3000", headers=True)  # <- widen to cover ALL columns

KEEP = ["Issue key", "Custom field (MAL Code)", "Custom field (Action)",
        "Custom field (Additional Information)", "Updated"]
ATT = re.compile(r"(?i)^attachment[\s.]*\d*$")   # Attachment / Attachment.1 / Attachment2
HIT = re.compile(r"(?i)AKCLDAC-\d+.*\.xlsx$")    # which filenames count

def norm(s):
    return re.sub(r"\s+", " ", str(s).replace("\u00a0", " ")).strip().casefold()

def inner(s):
    m = re.search(r"\((.*)\)", str(s))
    return norm(m.group(1)) if m else None

cols = list(df.columns)
ncols = [norm(c) for c in cols]

def find(target):
    t, ti = norm(target), inner(target)
    if t in ncols:
        return ncols.index(t)
    if ti:
        for i, c in enumerate(cols):                      # Custom field ( X ) variants
            if ncols[i].startswith("custom field") and inner(c) == ti:
                return i
        if ti in ncols:                                   # bare name, e.g. "MAL Code"
            return ncols.index(ti)
        for i, nc in enumerate(ncols):                    # loose contains, custom fields only
            if nc.startswith("custom field") and ti in nc:
                return i
    return None

keep_idx = {k: find(k) for k in KEEP}
missing = [k for k, v in keep_idx.items() if v is None]
att_idx = [i for i, nc in enumerate(ncols) if ATT.match(nc)]

if missing or not att_idx:
    diag = (["MISSING: " + m for m in missing]
            + (["MISSING: Attachment column(s)"] if not att_idx else [])
            + ["--- headers found in range ---"] + [str(c) for c in cols])
    result = pd.DataFrame({"Diagnostic": diag})
else:
    rows = []
    for _, r in df.iterrows():
        for i in att_idx:
            cell = r.iloc[i]
            if not isinstance(cell, str) or not cell.strip():
                continue
            for entry in cell.splitlines():
                parts = entry.split(";", 3)               # date ; uploader ; filename ; url
                if len(parts) < 3:
                    continue
                name = parts[2].strip()
                if HIT.search(name):
                    date = parts[0].strip().split(" ")[0].replace("/", "-")
                    rows.append([r.iloc[keep_idx["Issue key"]], name, date] +
                                [r.iloc[keep_idx[k]] for k in KEEP[1:]])
    result = pd.DataFrame(rows, columns=["Issue key", "Xls", "Date"] + KEEP[1:])

result