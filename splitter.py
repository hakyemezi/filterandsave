"""Pure file splitting helpers, independent of Streamlit."""
import io
import os
import re
import zipfile

import pandas as pd

MAX_UPLOAD_BYTES = 25 * 1024 * 1024
MAX_EXPANDED_BYTES = 100 * 1024 * 1024
MAX_ROWS = 200_000
MAX_GROUPS = 500
MAX_CELLS = 2_000_000


def safe_name(value):
    name = re.sub(r'[\x00-\x1f\\/:*?"<>|]', '_', str(value)).strip().strip(".' ")
    name = (name or 'unnamed')[:100]
    if name.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *[f'COM{i}' for i in range(1, 10)], *[f'LPT{i}' for i in range(1, 10)]}:
        name = '_' + name
    return name


def unique_name(value, used, limit=100, sheet=False):
    base = safe_name(value)
    if sheet:
        base = re.sub(r'[\[\]]', '_', base)
    base = base[:limit]
    name, counter = base, 1
    while name.casefold() in used:
        counter += 1
        suffix = f'_{counter}'
        name = base[:limit - len(suffix)] + suffix
    used.add(name.casefold())
    return name


def sheet_name(value, used):
    return unique_name(value, used, limit=31, sheet=True)


def validate_upload(data, filename):
    if not data:
        raise ValueError('The uploaded file is empty.')
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValueError('Upload limit: 25 MiB.')
    if filename.lower().endswith('.xlsx'):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if sum(item.file_size for item in archive.infolist()) > MAX_EXPANDED_BYTES:
                raise ValueError('Expanded workbook limit: 100 MiB.')


def read_uploaded_file(file_bytes, file_name, sheet=0, *, separator=None, encoding='utf-8-sig'):
    validate_upload(file_bytes, file_name)
    ext = os.path.splitext(file_name)[1].lower()
    buffer = io.BytesIO(file_bytes)
    if ext == '.xlsx':
        frame = pd.read_excel(buffer, sheet_name=sheet, nrows=MAX_ROWS + 1)
    elif ext == '.csv':
        frame = pd.read_csv(buffer, sep=separator, engine='python', encoding=encoding, nrows=MAX_ROWS + 1)
    elif ext == '.json':
        frame = pd.read_json(buffer)
    else:
        raise ValueError('Supported formats: XLSX, CSV, JSON.')
    if len(frame) > MAX_ROWS or frame.size > MAX_CELLS:
        raise ValueError('Table limit: 200,000 rows and 2,000,000 cells.')
    if frame.empty or not len(frame.columns):
        raise ValueError('The file contains no data rows.')
    return frame


def build_groups(df, split_columns, keep_columns, drop_empty):
    if not split_columns or not keep_columns:
        raise ValueError('Select grouping and output columns.')
    frame = df.dropna(subset=split_columns) if drop_empty else df
    grouped = frame.groupby(split_columns, dropna=False, sort=True, observed=True)
    if grouped.ngroups > MAX_GROUPS:
        raise ValueError(f'Group limit: {MAX_GROUPS}. Choose fewer grouping columns.')
    groups = []
    for keys, group in grouped:
        if not isinstance(keys, tuple):
            keys = (keys,)
        groups.append((' - '.join(safe_name(key) for key in keys), group[keep_columns]))
    return groups


def build_output(groups, delivery):
    if not groups or len(groups) > MAX_GROUPS or delivery not in (0, 1, 2):
        raise ValueError('Invalid output selection or group count.')
    output, used = io.BytesIO(), set()
    if delivery == 0:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for label, group in groups:
                group.to_excel(writer, sheet_name=sheet_name(label, used), index=False)
    else:
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
            for label, group in groups:
                name = unique_name(label, used)
                if delivery == 2:
                    archive.writestr(f'{name}.csv', group.to_csv(index=False).encode('utf-8-sig'))
                else:
                    buffer = io.BytesIO()
                    group.to_excel(buffer, index=False)
                    archive.writestr(f'{name}.xlsx', buffer.getvalue())
    return output.getvalue()
