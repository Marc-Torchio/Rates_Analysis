import pandas as pd
import table_script  # Assuming this is a custom module you've created for handling specific table operations.

def individual_flatfile(URRT_folder=r'C:\Users\A654219\Documents\GA\URRTs',
                        plans_folder=r"C:\Users\A654219\Documents\GA\Plans & Benefits Templates",
                        name_mapping_path=r"C:\Users\A654219\Documents\GA\name_mapping.xlsx"):
    """
    Process individual flatfiles by merging various data sources into a comprehensive DataFrame.

    Parameters:
    - URRT_folder (str): Path to the folder containing URRT files.
    - plans_folder (str): Path to the folder containing Plans & Benefits Templates.
    - name_mapping_path (str): Path to the Excel file containing name mappings.

    Returns:
    - The merged dataframe combining URRT data, Network ID, Network Name, and Rates
    """
    
    # Load URRT table data
    df = table_script.URRT_Table(URRT_folder)
    
    # Load and prepare name mappings
    names = pd.read_excel(name_mapping_path)
    names['HIOS_ID'] = names['HIOS_ID'].astype(str)  # Ensure HIOS_ID is treated as a string for consistent merging
    
    # Load and filter Plans table data
    plans = table_script.Plan_Table(plans_folder)
    plans = plans[['Plan ID', 'Network ID']]  # Keep only the necessary columns
    
    # Load Network table data
    network_key = table_script.Network_Table(r"C:\Users\A654219\Documents\GA\Network Templates")
    
    # Merge loaded dataframes on specified keys, using 'left' join to preserve the left DataFrame's rows
    new_df = pd.merge(df, names, on='HIOS_ID', how='left')  # Merge URRT data with name mappings
    new_df = pd.merge(new_df, plans, on='Plan ID', how='left')  # Merge with plans
    new_df = pd.merge(new_df, network_key, on=['HIOS_ID', 'Network ID'], how='left')  # Finally, merge with network keys
    
    # Return the original df, names, plans, and network_key for further use or inspection
    return new_df, names, plans, network_key