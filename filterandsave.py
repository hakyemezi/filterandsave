import streamlit as st
import pandas as pd
import io
import os
from splitter import read_uploaded_file, build_groups, build_output, validate_upload

from translations import LANGUAGES, TRANSLATIONS, DOT_SEPARATOR, SPACE_SEPARATOR

st.set_page_config(page_title="Split a spreadsheet by column", page_icon="✂️", layout="wide")

# The language has to be picked before any text is written, so the selector
# comes first. set_page_config cannot be translated, it runs before this.
#
# Every language is listed with its flag rather than hidden behind a dropdown,
# so a visitor can see their own language without opening anything. Streamlit
# has already written the new choice into session state by the time this runs,
# which is why the label can be shown in the language being switched to.
current_language = st.session_state.get("language", "en")

language = st.sidebar.radio(
    "🌐 " + TRANSLATIONS[current_language]["language"],
    list(LANGUAGES.keys()),
    format_func=lambda code: f"{LANGUAGES[code][0]} {LANGUAGES[code][1]}",
    key="language",
)


def t(key):
    # Fall back to English so a missing translation never breaks the page
    return TRANSLATIONS[language].get(key) or TRANSLATIONS["en"][key]


def number(value):
    # 1,234 in English, 1.234 in Turkish, German, Spanish and Italian,
    # 1 234 in French
    text = f"{value:,}"
    if language in DOT_SEPARATOR:
        return text.replace(",", ".")
    if language in SPACE_SEPARATOR:
        return text.replace(",", " ")
    return text


st.title(t("title"))
st.caption(t("caption"))

uploaded_file = st.file_uploader(t("uploader"), type=["xlsx", "csv", "json"])

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()
    file_type = os.path.splitext(uploaded_file.name)[1].lower()

    sheet = 0
    separator, encoding = None, 'utf-8-sig'
    try:
        validate_upload(file_bytes, uploaded_file.name)
        if file_type == '.xlsx':
            with pd.ExcelFile(io.BytesIO(file_bytes)) as workbook:
                sheet_names = workbook.sheet_names
            if len(sheet_names) > 1:
                sheet = st.selectbox(t('sheet_pick'), sheet_names)
        elif file_type == '.csv':
            separator = st.selectbox(t('csv_separator'), [None, ',', ';', '\t', '|'],
                                     format_func=lambda value: t('automatic') if value is None else repr(value))
            encoding = st.selectbox(t('csv_encoding'), ['utf-8-sig', 'cp1254', 'latin-1'])
        df = read_uploaded_file(file_bytes, uploaded_file.name, sheet,
                                separator=separator, encoding=encoding)
    except Exception as error:
        st.error(t('read_error').format(error=str(error)))
        st.stop()

    st.success(t("loaded").format(rows=number(len(df)), cols=len(df.columns)))
    with st.expander(t("preview")):
        st.dataframe(df.head(50), use_container_width=True)

    st.subheader(t("step1"))

    column_list = list(df.columns)
    split_columns = st.multiselect(
        t("split_label"),
        column_list,
        default=column_list[:1],
        help=t("split_help"),
    )

    if split_columns:

        drop_empty = st.checkbox(t("drop_empty"), value=True)

        keep_columns = st.multiselect(
            t("keep_label"),
            column_list,
            default=column_list,
            help=t("keep_help"),
        )

        if not keep_columns:
            st.warning(t("keep_warn"))
            st.stop()

        try:
            groups = build_groups(df, split_columns, keep_columns, drop_empty)
        except ValueError as error:
            st.error(t('read_error').format(error=str(error)))
            st.stop()

        if not groups:
            st.warning(t("no_groups"))
            st.stop()

        st.subheader(t("step2"))

        summary = pd.DataFrame(
            {t("col_group"): [label for label, _ in groups],
             t("col_rows"): [len(group) for _, group in groups]}
        )
        covered = int(summary[t("col_rows")].sum())

        left, right = st.columns([1, 2])
        with left:
            st.metric(t("m_groups"), number(len(groups)))
            st.metric(t("m_rows"), number(covered))
            st.metric(t("m_largest"), t("rows_value").format(n=number(int(summary[t("col_rows")].max()))))
            skipped = len(df) - covered
            if skipped:
                st.metric(t("m_skipped"), number(skipped))
        with right:
            st.dataframe(summary, use_container_width=True, hide_index=True, height=260)

        st.subheader(t("step3"))

        # Selected by position rather than by label, so the choice keeps
        # working whatever language the interface is in
        delivery = st.radio(
            t("output_label"),
            [0, 1, 2],
            format_func=lambda index: t(f"opt{index}"),
            help=t("output_help"),
        )

        if delivery == 0 and len(groups) > 200:
            st.info(t("many_sheets").format(n=number(len(groups))))

        if st.button(t("build"), type="primary"):

            with st.spinner(t("building").format(n=number(len(groups)))):

                try:
                    output = build_output(groups, delivery)
                except Exception as error:
                    st.error(t('read_error').format(error=str(error)))
                    st.stop()
                st.download_button(
                    t('dl_workbook') if delivery == 0 else t('dl_zip'), output,
                    file_name='split.xlsx' if delivery == 0 else 'split.zip',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                         if delivery == 0 else 'application/zip',
                )
            st.success(t('ready'))
