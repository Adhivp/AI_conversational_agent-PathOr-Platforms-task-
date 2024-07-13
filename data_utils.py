import pandas as pd

def read_excel(file_path, sheet_name=0):
    """
    Reads an Excel file and returns the data from the specified sheet.
    
    :param file_path: Path to the Excel file.
    :param sheet_name: Name or index of the sheet to read (default is the first sheet).
    :return: DataFrame containing the data from the specified sheet.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def read_csv(file_path):
    """
    Reads a CSV file and returns the data.
    
    :param file_path: Path to the CSV file.
    :return: DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
def extract_data(df, row_index=None, column_name=None):
    """
    Extracts data from a specified row and column in a DataFrame.
    
    :param df: DataFrame to extract data from.
    :param row_index: Index of the row to extract data from (optional).
    :param column_name: Name of the column to extract data from (optional).
    :return: Extracted data from the specified row and column, or the full DataFrame if no row/column is specified.
    """
    try:
        if row_index is not None and column_name is not None:
            return df.loc[row_index, column_name]
        elif row_index is not None:
            return df.iloc[row_index]
        elif column_name is not None:
            return df[column_name]
        else:
            return df
    except KeyError:
        print(f"Column '{column_name}' not found in DataFrame.")
        return None
    except IndexError:
        print(f"Row index '{row_index}' is out of bounds.")
        return None