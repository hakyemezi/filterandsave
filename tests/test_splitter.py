from pathlib import Path
import io
import zipfile
import pandas as pd
import pytest
from splitter import build_groups, build_output, read_uploaded_file, unique_name, sheet_name


def test_collisions_casefold_and_truncation():
    for naming in [unique_name, sheet_name]:
        used = set()
        names = [naming(value, used) for value in ['A', 'A', 'A_2', 'a', 'X'*120, 'X'*120, "'", '[]']]
        assert len({value.casefold() for value in names}) == len(names)
        assert all(len(value) <= (31 if naming == sheet_name else 100) for value in names)


@pytest.mark.parametrize('delivery', [0, 1, 2])
def test_outputs_preserve_all_groups(delivery):
    groups = [(name, pd.DataFrame({'value': [index]})) for index, name in enumerate(['A', 'A', 'A_2', 'a'])]
    result = build_output(groups, delivery)
    if delivery == 0:
        sheets = pd.read_excel(io.BytesIO(result), sheet_name=None)
        assert len(sheets) == 4
        assert sorted(int(frame.iloc[0, 0]) for frame in sheets.values()) == list(range(4))
    else:
        with zipfile.ZipFile(io.BytesIO(result)) as archive:
            assert len(archive.namelist()) == len(set(archive.namelist())) == 4
            values = []
            for name in archive.namelist():
                data = io.BytesIO(archive.read(name))
                frame = pd.read_csv(data) if delivery == 2 else pd.read_excel(data)
                values.append(int(frame.iloc[0, 0]))
            assert sorted(values) == list(range(4))


def test_csv_options_and_missing_group_retention():
    data = 'grup;değer\nİş;1\n;2\n'.encode('cp1254')
    frame = read_uploaded_file(data, 'input.csv', encoding='cp1254', separator=';')
    assert frame.columns.tolist() == ['grup', 'değer']
    assert len(build_groups(frame, ['grup'], ['değer'], False)) == 2
    assert len(build_groups(frame, ['grup'], ['değer'], True)) == 1


def test_empty_corrupt_and_excess_groups():
    with pytest.raises(ValueError): read_uploaded_file(b'', 'bad.csv')
    with pytest.raises(zipfile.BadZipFile): read_uploaded_file(b'not excel', 'bad.xlsx')
    frame = pd.DataFrame({'x': range(501)})
    with pytest.raises(ValueError, match='Group limit'): build_groups(frame, ['x'], ['x'], False)


def test_auto_separator():
    frame = read_uploaded_file(b'name;value\na;1\nb;2\n', 'test.csv')
    assert frame.shape == (2, 2)


def test_app_starts_without_upload():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / 'filterandsave.py').run()
    assert not app.exception
