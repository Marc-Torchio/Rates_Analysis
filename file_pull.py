import pandas as pd
import os
import shutil
import re

files = ['Service Area', 'URRT', 'Rates Table Template', 'Network Template','Plans & Benefits Template']

def Rates_File_Puller(type, source_folder=r"Z:\Strategy Groups\Individual Plans\Rates Analysis\2024\GA\Preliminary Rates Analysis\Rate Filings", target_folder=r"C:\Users\A654219\Documents\GA"):
    new_folder_name = type + 's'
    try:
        shutil.rmtree(os.path.join(target_folder,new_folder_name))
    except Exception as e:
        print('Folder not initialized')
    
    # Initial size counters
    total_tries = 0
    successes = 0
    failures = 0
    
    # Define your regex pattern based on the 'type'
    regex_patterns = {
        'Rates Table Template': rf'\d{{4}}\s{type}.*',
        'Service Area': rf'\d{{4}}\s{type}.*',
        'Network Template': rf'\d{{4}}\s{type}.*',
        'Plans & Benefits Template': rf'\d{{4}}\s{type}.*',
        'Service Area': rf'\d{{4}}\s{type}.*',
        'URRT': '.*Instructions can be found in cells P1 through P6.*'
    }
    
    # Corresponding sheet names or indexes
    sheet_names = {
        'Rates Table Template': 'Rate Table',
        'Service Area': 'Service Area',
        'Network Template': 'Networks',
        'Plans & Benefits Template': 'Benefits Package 1',
        'Service Area': 'Service Areas',
        'URRT': 1
    }
    
    regex_pattern = regex_patterns[type]
    sheet_n = sheet_names[type]

    # Mapping to hold the most recent file info for each unique case
    most_recent_files = {}

    # Function to check and update the most recent file mapping
    def check_and_update_most_recent(file_path, modification_time):
        # Assuming the file's uniqueness can be determined from its path or a portion thereof
        unique_identifier = os.path.basename(file_path)  # Adjust as necessary for uniqueness
        if unique_identifier not in most_recent_files or modification_time > most_recent_files[unique_identifier]['modification_time']:
            most_recent_files[unique_identifier] = {
                'file_path': file_path,
                'modification_time': modification_time
            }
    
        # Function to process each file
    def process_file(file_path, target_folder, sheet_n):
        nonlocal total_tries, successes, failures  # Use nonlocal to modify these counters defined in the enclosing function
        
        
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

    # Iterate over the folders and files, updating the most recent mapping
    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                total_tries += 1  # Increment tries counter
                if filename.endswith('.xls') or filename.endswith('.xlsm'):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        # Modification time for the current file
                        modification_time = os.path.getmtime(file_path)
                        # Read the file to check if it matches the regex
                        df = pd.read_excel(file_path, sheet_name=sheet_n, header=None)
                        cell_value = df.iloc[0, 0]
                        if re.match(regex_pattern, str(cell_value)):
                            check_and_update_most_recent(file_path, modification_time)
                        else:
                            failure +=1 # Increment failures counter
                    except Exception as e:
                        failures += 1  # Increment failures counter
                else:
                    failures += 1
        else:
            failures += 1

    # Now process only the most recent files
    for file_info in most_recent_files.values():
        # Extract the file_path from file_info dictionary
        file_path = file_info['file_path']
        # Call process_file with the correct arguments
        process_file(file_path, target_folder, sheet_n)

    # You might want to adjust the success, failure, and total tries counters accordingly
    print(f'Done! Total files tried: {total_tries}, Successes: {successes}, Failures: {failures}')
    return os.path.join(target_folder, new_folder_name)