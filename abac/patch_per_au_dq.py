"""
Patch ABAC_DQ_Per_AU_Checks.ipynb to:
1. Add DB = 'hive_metastore.ra_adido_2025' to the config cell
2. Replace all hardcoded 'hive_metastore.ra_adido_2025' with {DB}
3. Convert plain ''' strings to f''' where needed for {DB} interpolation

Run from this directory:
    python patch_per_au_dq.py
"""

import json
import os
import re
import shutil

NOTEBOOK_PATH = os.path.join(os.path.dirname(__file__), 'ABAC_DQ_Per_AU_Checks.ipynb')
BACKUP_PATH = NOTEBOOK_PATH + '.bak'
HARDCODED_DB = 'hive_metastore.ra_adido_2025'

def patch_notebook():
    # Backup first
    shutil.copy2(NOTEBOOK_PATH, BACKUP_PATH)
    print(f'Backup created: {BACKUP_PATH}')

    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']
    changes = []

    for i, cell in enumerate(cells):
        if cell['cell_type'] != 'code':
            continue

        source = ''.join(cell['source'])

        # --- CELL: CONFIG ---
        # Add DB variable after SNAPSHOT_CATALOGUE_NAME
        if "SNAPSHOT_CATALOGUE_NAME = 'RA_FY_2025'" in source and 'DB =' not in source:
            new_source = source.replace(
                "SNAPSHOT_CATALOGUE_NAME = 'RA_FY_2025'",
                "SNAPSHOT_CATALOGUE_NAME = 'RA_FY_2025'\nDB = 'hive_metastore.ra_adido_2025'"
            )
            # Also add DB to the print statements
            new_source = new_source.replace(
                "print(f'Results Table: {TABLE_NAME}')",
                "print(f'DB: {DB}')\nprint(f'Results Table: {TABLE_NAME}')"
            )
            cell['source'] = _to_source_lines(new_source)
            changes.append(f'Cell {i}: Added DB variable to config')

        # --- ALL CODE CELLS: Replace hardcoded DB refs ---
        elif HARDCODED_DB in source:
            new_source = source

            # Replace hardcoded DB path with {DB}
            new_source = new_source.replace(HARDCODED_DB + '.', '{DB}.')

            # Now we need to convert plain ''' or """ strings to f-strings
            # where {DB} was just introduced.
            # Pattern: find variable assignments like xxx_sql = ''' or spark.sql('''
            # that now contain {DB} but aren't f-strings.

            # Handle: xxx_sql = '''...''' -> xxx_sql = f'''...'''
            new_source = _ensure_fstrings(new_source)

            if new_source != source:
                # When converting to f-string, single quotes in LIKE patterns
                # like '%-%-%' need to be escaped. But in triple-quoted f-strings,
                # single quotes are fine — no escaping needed.
                cell['source'] = _to_source_lines(new_source)
                changes.append(f'Cell {i}: Replaced {HARDCODED_DB} with {{DB}}')

    # Write patched notebook
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write('\n')

    print(f'\nPatched {len(changes)} cells:')
    for c in changes:
        print(f'  [OK] {c}')
    print(f'\nNotebook saved: {NOTEBOOK_PATH}')


def _ensure_fstrings(source: str) -> str:
    """Convert plain triple-quoted strings to f-strings where they contain {DB}."""

    # Pattern 1: variable_sql = '''...''' or variable_sql = """..."""
    # These are multi-line SQL string assignments
    source = re.sub(
        r"""(\w+_sql\s*=\s*)('{3}|"{3})""",
        lambda m: m.group(1) + 'f' + m.group(2) if '{DB}' in _find_string_content(source, m.start()) else m.group(0),
        source
    )

    # Pattern 2: spark.sql('''...''') that aren't already f-strings
    # Look for spark.sql( NOT preceded by f
    source = re.sub(
        r"""(spark\.sql\()(\s*)('{3}|"{3})""",
        lambda m: m.group(1) + m.group(2) + 'f' + m.group(3) if '{DB}' in _find_string_content(source, m.start()) else m.group(0),
        source
    )

    return source


def _find_string_content(source: str, start_pos: int) -> str:
    """Extract ~500 chars after start_pos to check if {DB} is in the string."""
    return source[start_pos:start_pos + 2000]


def _to_source_lines(source: str) -> list:
    """Convert a source string back to notebook source format (list of lines with \\n)."""
    lines = source.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + '\n')
        else:
            result.append(line)
    return result


if __name__ == '__main__':
    patch_notebook()
