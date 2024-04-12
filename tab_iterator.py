import pandas as pd
import re

def concat_matching_sheets(excel_path):
    pattern = re.compile(r'Benefits Package\s\d')
    dfs = []

    xls = pd.ExcelFile(excel_path)

    for sheet_name in xls.sheet_names:
        if pattern.match(sheet_name):
            # Specify columns to read: A through AD
            use_cols = range(0, 30)  # 0-indexed, so 30 is not included, which corresponds to columns A-AD
            
            # Calculate the number of rows to read to exclude data below row 57
            nrows_to_read = 50  # Since headers are on row 6, and we want up to row 57
            
            # Read the sheet into a DataFrame with headers starting at row 6 (index 5 since it's 0-indexed),
            # only consider columns A through AD, and limit the number of rows read
            df = pd.read_excel(xls, sheet_name=sheet_name, header=6, usecols=use_cols, nrows=nrows_to_read)
            
            # Drop rows where all considered elements are NaN
            df = df.dropna(how='all').reset_index(drop=True)

            dfs.append(df)

    concatenated_df = pd.concat(dfs, ignore_index=True)

    return concatenated_df

def tab_creator(df):
    # Path to save the Excel file
    output_file = 'Flat_File.xlsx'

    # Using ExcelWriter to write each group to a different sheet
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write the entire DataFrame to a sheet named 'Flat File'
        df.to_excel(writer, sheet_name='Flat File', index=False)
        # Get unique carriers and iterate over them
        for carrier in df['Short Carrier'].unique():
            # Filter the DataFrame based on the carrier
            filtered_df = df[df['Short Carrier'] == carrier]
            # Write the filtered DataFrame to a sheet named after the carrier
            filtered_df.to_excel(writer, sheet_name=carrier, index=False)
