# =====================================================================
# Python in Excel - v7 (FINAL)
# Replace the whole contents of the =PY( ) cell with everything below.
#
# Fix vs v6 (why some tickets came back empty):
#   Some cells hold SEVERAL attachment entries run together on one
#   line (previous entry's URL, then a space, then the next entry's
#   date). v6 only read the first entry per line, so an xlsx sitting
#   behind a .msg or .csv in the same cell was never seen. v7 regex-
#   scans every cell for each "date;uploader;filename;" occurrence,
#   so every entry is found regardless of how they're separated.
#   Also: DAC-name preference now catches underscore style
#   ("Data_Access_Framework_...").
#
# Current behaviour:
#   - Reads the export from sheet "in", range A1:RC939.
#   - Keeps ONLY tickets whose Reporter is one of: TAH1775, TAJ7583,
#     TAM0124 (case-insensitive, bare ID or "Name (ID)" style).
#   - Only .xlsx files count.
#   - Exactly ONE row per ticket: DAC / DAF / Data Access-named files
#     beat other xlsx; within that the LATEST upload wins. Tickets
#     with no xlsx get a blank Xls/Date row (= missing DAC record).
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
HIT    = re.compile(r"(?i)\.xlsx$")                                       # xlsx only
PREFER = re.compile(r"(?i)(?<![a-z])(dac|daf)(?![a-z])|data[ _]access")   # DAC-record name hints
ENTRY  = re.compile(                                                      # one attachment entry:
    r"(\d{1,2}/[A-Za-z]{3}/\d{2}"                                         #   date 17/Feb/26
    r"(?:\s+\d{1,2}:\d{2}\s*[AP]M)?)"                                     #   optional time 9:40 AM
    r"\s*;\s*([^;]*?)\s*;\s*([^;]*?)\s*;")                                #   ;uploader;filename;

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
            for m in ENTRY.finditer(cell):
                dstamp, name = m.group(1), m.group(3).strip()
                if HIT.search(name):
                    hits.append((bool(PREFER.search(name)), stamp(dstamp),
                                 dstamp.strip().split(" ")[0].replace("/", "-"),
                                 name, len(hits)))
        if hits:
            best = max(hits, key=lambda h: (h[0], h[1], h[4]))
            name, date = best[3], best[2]
        else:
            name, date = "", ""
        rows.append([ik, name, date] + [r.iloc[keep_idx[k]] for k in KEEP[1:]])
    result = pd.DataFrame(rows, columns=["Issue key", "Xls", "Date"] + KEEP[1:])

result