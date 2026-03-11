import pandas as pd


def load_dataframe(uploaded_file, sheet_name=None):

    name = uploaded_file.name.lower()

    if name.endswith(".csv"):

        encodings = ["utf-8", "utf-8-sig", "latin1"]

        for enc in encodings:
            try:
                return pd.read_csv(uploaded_file, encoding=enc)
            except:
                continue

        raise ValueError("Could not read CSV file")

    elif name.endswith(".xlsx"):

        if sheet_name:
            return pd.read_excel(uploaded_file, sheet_name=sheet_name)

        return pd.read_excel(uploaded_file)

    else:
        raise ValueError("Unsupported file type")


def list_excel_sheets(uploaded_file):

    xls = pd.ExcelFile(uploaded_file)

    return xls.sheet_names
