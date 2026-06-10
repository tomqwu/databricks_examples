# =====================================================================
# Python in Excel - v13 (FINAL)
# Replace the whole contents of the =PY( ) cell with everything below.
#
# Change vs v12:
#   Back to ONE xlsx per ticket: the LATEST attached one by upload
#   timestamp. The space/+ canonicalisation stays, so a file that
#   appears in both forms counts once and the readable space variant
#   is what gets shown.
#
# Current behaviour:
#   - Reads the export from sheet "in", range A1:ZZ1000
#     (Ctrl+End on "in" gives the true bottom-right cell to use).
#   - Keeps ONLY tickets whose Reporter is one of: TAH1775, TAJ7583,
#     TAM0124 (case-insensitive, bare ID or "Name (ID)" style).
#   - Only .xlsx files count.
#   - Xls = the latest xlsx attached to the ticket; Date = its upload
#     date (dd-Mmm-yy). One row per ticket; blank Xls/Date = ticket
#     has no xlsx anywhere in the row.
#   - Attachments are found by scanning EVERY cell in the row for the
#     date;uploader;filename; pattern (shifted rows, jammed entries,
#     AM/PM or 24-hour timestamps).
#   - MAL Code / Action / Additional Information recovered by value
#     signature when the header position doesn't look right; literal
#     "None" never carried through.
#   - Output: Issue key | Xls | Date | Custom field (MAL Code) |
#     Custom field (Action) | Custom field (Additional Information) |
#     Updated | Reporter
# =====================================================================

import pandas as pd
import re
from datetime import datetime

df = xl("in!A1:ZZ1000", headers=True)   # <- Ctrl+End on "in" gives the true bottom-right cell

KEEP = ["Issue key", "Custom field (MAL Code)", "Custom field (Action)",
        "Custom field (Additional Information)", "Updated", "Reporter"]
REPORTERS = ["TAH1775", "TAJ7583", "TAM0124"]   # only these; empty list = keep all
HIT   = re.compile(r"(?i)\.xlsx$")                                        # xlsx only
ENTRY = re.compile(                                                       # one attachment entry:
    r"(\d{1,2}/[A-Za-z]{3}/\d{2}"                                         #   date 17/Feb/26
    r"(?:\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)?)"                     #   time 9:40 AM / 13:53
    r"\s*;\s*([^;]*?)\s*;\s*([^;]*?)\s*;")                                #   ;uploader;filename;

# value signatures used to recover shifted fields
SIGS = {
    "Custom field (MAL Code)":               re.compile(r"(?i)^\s*MAL Code\s*:"),
    "Custom field (Action)":                 re.compile(r"(?i)^\s*PII Data\s*:"),
    "Custom field (Additional Information)": re.compile(r"(?i)^\s*Highest Security Classification"),
}

def norm(s):
    return re.sub(r"\s+", " ", str(s).replace("\u00a0", " ")).strip().casefold()

def inner(s):
    m = re.search(r"\((.*)\)", str(s))
    return norm(m.group(1)) if m else None

def stamp(s):
    s = re.sub(r"\s+", " ", str(s).strip())
    for f in ("%d/%b/%y %I:%M %p", "%d/%b/%y %H:%M", "%d/%b/%y %H:%M:%S", "%d/%b/%y"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return datetime.min

def canon(name):
    """Canonical filename: URL-encoded spaces (+ / %20) = real spaces, case-insensitive."""
    s = name.replace("%20", " ").replace("+", " ")
    return re.sub(r"\s+", " ", s).strip().casefold()

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

if missing:
    diag = (["MISSING: " + m for m in missing]
            + ["--- headers found in range ---"] + [str(c) for c in cols])
    result = pd.DataFrame({"Diagnostic": diag})
else:
    def sig_value(r, key):
        """Header-positioned value if it matches the signature, else scan the row."""
        sig = SIGS[key]
        v = r.iloc[keep_idx[key]]
        s = v.strip() if isinstance(v, str) else ""
        if sig.match(s):
            return s
        for v2 in r:
            if isinstance(v2, str) and sig.match(v2.strip()):
                return v2.strip()
        return ""

    rows = []
    for _, r in df.iterrows():
        ik = r.iloc[keep_idx["Issue key"]]
        if not isinstance(ik, str) or not ik.strip():
            continue                                  # skip range padding
        rep = norm(r.iloc[keep_idx["Reporter"]])
        if REPORTERS and not any(x.casefold() in rep for x in REPORTERS):
            continue                                  # not one of the 3 reporters
        hits = {}                                     # (canon, date) -> (dt, date, display_name)
        for v in r:                                   # scan EVERY cell, header-independent
            if not isinstance(v, str) or ";" not in v:
                continue
            for m in ENTRY.finditer(v):
                dstamp, name = m.group(1), m.group(3).strip()
                if not HIT.search(name):
                    continue
                date = dstamp.strip().split(" ")[0].replace("/", "-")
                key = (canon(name), date)
                if key not in hits:
                    hits[key] = (stamp(dstamp), date, name)
                elif name.count("+") < hits[key][2].count("+"):
                    hits[key] = (hits[key][0], date, name)   # prefer readable space variant
        if hits:
            latest = max(hits.values(), key=lambda h: (h[0], -h[2].count("+")))
            name, date = latest[2], latest[1]
        else:
            name, date = "", ""
        rows.append([ik, name, date,
                     sig_value(r, "Custom field (MAL Code)"),
                     sig_value(r, "Custom field (Action)"),
                     sig_value(r, "Custom field (Additional Information)"),
                     r.iloc[keep_idx["Updated"]],
                     r.iloc[keep_idx["Reporter"]]])
    result = pd.DataFrame(rows, columns=["Issue key", "Xls", "Date"] + KEEP[1:])

result