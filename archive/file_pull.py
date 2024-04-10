
def file_sparse(type, source_folder=r"Z:\Strategy Groups\Individual Plans\Rates Analysis\2024\GA\Preliminary Rates Analysis\Rate Filings", target_folder=r"C:\Users\A654219\Documents\GA"):
    import pandas as pd
    import os
    import shutil
    import re
    
    new_folder_name = type + 's'
    try:
        shutil.rmtree(os.path.join(target_folder,new_folder_name))
    except:
        print('Folder not initiatilized')
    
    # Initial size counters
    total_tries = 0
    successes = 0
    failures = 0

    if type == 'Rates Table Template':
        # Define your regex pattern
        regex_pattern = rf'\d{{4}}\s{type}.*'

        # Need to specify sheetname to override the need for macros 
        sheet_n = 'Rate Table'
    elif type == 'Network Table Template':
        # Define your regex pattern
        regex_pattern = rf'\d{{4}}\s{type}.*'

        # Need to specify sheetname to override the need for macros 
        sheet_n = 'Network Table'
    elif type == 'Service Area':
        # Define your regex pattern
        regex_pattern = rf'\d{{4}}\s{type}.*'

        # Need to specify sheetname to override the need for macros 
        sheet_n = 'Service Area'
    elif type == 'Network Template':
        # Define your regex pattern
        regex_pattern = rf'\d{{4}}\s{type}.*'

        # Need to specify sheetname to override the need for macros 
        sheet_n = 'Networks'
    elif type == 'Plans & Benefits Template':
        # Define your regex pattern
        regex_pattern = rf'\d{{4}}\s{type}.*'

        # Need to specify sheetname to override the need for macros 
        sheet_n = 'Benefits Package 1'
    
    elif type == 'URRT':
        # Define your regex pattern
        regex_pattern = '.*Instructions can be found in cells P1 through P6.*'

        # Need to specify sheetname to override the need for macros 
        sheet_n = 1


    # Function to process each file
    def process_file(file_path, target_folder, sheet_n):
        nonlocal total_tries, successes, failures  # Use nonlocal to modify these counters defined in the enclosing function
        
        total_tries += 1  # Increment tries counter
        try:
            # Read the file
            df = pd.read_excel(file_path, sheet_name=sheet_n, header=None)
            
            # Get the value from the criteria cell
            cell_value = df.iloc[0,0]
            
            # Use regex to check if the cell value matches the pattern
            if re.match(regex_pattern, str(cell_value)):
                
                # Ensure the target folder exists
                new_folder_path = os.path.join(target_folder, new_folder_name)
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                
                # Extract the name of the folder the file is currently in
                original_folder_name = os.path.basename(os.path.dirname(file_path))

                # Create the new filename by appending "type" to the folder name
                new_filename = f"{original_folder_name}_{type}{os.path.splitext(file_path)[1]}"  # Preserves the original file extension

                # Construct the full path for the destination, including the new filename
                destination_path = os.path.join(target_folder, new_folder_name, new_filename)

                # Copy the file to the new folder, renaming it in the process
                shutil.copy(file_path, destination_path)
                print(f'Copied to: {new_folder_path}')
                successes += 1  # Increment successes counter
            else:
                # If the regex does not match, you can count it as a failure or just ignore
                failures += 1  # Optional: Increment failures counter if non-match is considered a failure
        except Exception as e:
            failures += 1  # Increment failures counter

    # Iterate over the folders in the source folder
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path):
            # Iterate over the files within each folder
            for filename in os.listdir(folder_path):
                if filename.endswith('.xls') or filename.endswith('.xlsm'):  # Check for both .xls and .xlsm files
                    file_path = os.path.join(folder_path, filename)
                    process_file(file_path, target_folder, sheet_n)

    # Summary of processing
    print(f'Done! Total files tried: {total_tries}, Successes: {successes}, Failures: {failures}')
    return os.path.join(target_folder, new_folder_name)


def extract_all(types, source, destination):
    for type in types:
        file_sparse(type, source, destination) 

