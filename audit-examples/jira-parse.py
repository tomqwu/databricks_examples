# =====================================================================
# Python in Excel - v6 (FINAL)
# Replace the whole contents of the =PY( ) cell with everything below.
#
# Current behaviour:
#   - Reads the export from sheet "in", range A1:RC939.
#   - Keeps ONLY tickets whose Reporter is one of: TAH1775, TAJ7583,
#     TAM0124 (per Patty). Matching is case-insensitive and works
#     whether the cell holds the bare ID or "Name (ID)" style.
#   - Scans every Attachment column; only .xlsx files count.
#   - Exactly ONE row per ticket: names signalling a DAC record
#     (DAC / DAF / "Data Access") beat other xlsx, and within that
#     the LATEST upload wins. Tickets with no xlsx get a blank
#     Xls/Date row, so blanks = missing DAC record.
#   - Output: Issue key | Xls | Date | Custom field (MAL Code) |
#     Custom field (Action) | Custom field (Additional Information) |
#     Updated | Reporter
#   - If expected columns can't be found, spills a Diagnostic column
#     listing the real headers instead of erroring.
# =====================================================================

import pandas as pd
import re
from datetime import datetime

df = xl("in!A1:RC939", headers=True)   # <- export range

KEEP = ["Issue key", "Custom field (MAL Code)", "Custom field (Action)",
        "Custom field (Additional Information)", "Updated", "Reporter"]
REPORTERS = ["TAH1775", "TAJ7583", "TAM0124"]   # only these; empty list = keep all
HIT    = re.compile(r"(?i)\.xlsx$")                                   # xlsx only
PREFER = re.compile(r"(?i)(?<![a-z])(dac|daf)(?![a-z])|data access")  # DAC-record name hints

def norm(s):
    return re.sub(r"\s+", " ", str(s).replace("\u00a0", " ")).strip().casefold()

def inner(s):
    m = re.search(r"\((.*)\)", str(s))
    return norm(m.group(1)) if m else None

def stamp(s):
    s = re.sub(r"\s+", " ", str(s).strip())
    for f in ("%d/%b/%y %I:%M %p", "%d/%b/%y"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return datetime.min

cols = list(df.columns)
ncols = [norm(c) for c in cols]

def find(target):
    t, ti = norm(target), inner(target)
    if t in ncols:
        return ncols.index(t)
    if ti:
        for i, c in enumerate(cols):
            if ncols[i].startswith("custom field") and inner(c) == ti:
                return i
        if ti in ncols:
            return ncols.index(ti)
        for i, nc in enumerate(ncols):
            if nc.startswith("custom field") and ti in nc:
                return i
    return None

keep_idx = {k: find(k) for k in KEEP}
missing = [k for k, v in keep_idx.items() if v is None]
att_idx = [i for i, nc in enumerate(ncols) if nc.startswith("attachment")]

if missing or not att_idx:
    diag = (["MISSING: " + m for m in missing]
            + (["MISSING: Attachment column(s)"] if not att_idx else [])
            + ["--- headers found in range ---"] + [str(c) for c in cols])
    result = pd.DataFrame({"Diagnostic": diag})
else:
    rows = []
    for _, r in df.iterrows():
        ik = r.iloc[keep_idx["Issue key"]]
        if not isinstance(ik, str) or not ik.strip():
            continue                                  # skip range padding
        rep = norm(r.iloc[keep_idx["Reporter"]])
        if REPORTERS and not any(x.casefold() in rep for x in REPORTERS):
            continue                                  # not one of the 3 reporters
        hits = []                                     # (preferred, dt, date_str, name, seq)
        for i in att_idx:
            cell = r.iloc[i]
            if not isinstance(cell, str) or not cell.strip():
                continue
            for entry in cell.splitlines():
                parts = entry.split(";", 3)           # date ; uploader ; filename ; url
                if len(parts) < 3:
                    continue
                name = parts[2].strip()
                if HIT.search(name):
                    hits.append((bool(PREFER.search(name)), stamp(parts[0]),
                                 parts[0].strip().split(" ")[0].replace("/", "-"),
                                 name, len(hits)))
        if hits:
            best = max(hits, key=lambda h: (h[0], h[1], h[4]))
            name, date = best[3], best[2]
        else:
            name, date = "", ""
        rows.append([ik, name, date] + [r.iloc[keep_idx[k]] for k in KEEP[1:]])
    result = pd.DataFrame(rows, columns=["Issue key", "Xls", "Date"] + KEEP[1:])

result