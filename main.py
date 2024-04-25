# Importing dependent packages 
import timeit
import warnings

# Importing necessary scripts from current repo
import table_script
import file_pull


# Removing warngings 
warnings.filterwarnings("ignore", category=UserWarning)



def Comp_File_Pull():
    template_dict = {}
    for temp in file_pull.files:
        new_folder = file_pull.Rates_File_Puller(type=temp, source_folder=r"Z:\Strategy Groups\SBU\Rates Analysis\2024\GA\Preliminary\Filings")
        template_dict[temp] = new_folder
    return template_dict

def comp_file_pull_wrapper():
    return Comp_File_Pull()

def rates_analysis_wrapper():
    templates = comp_file_pull_wrapper() # Call the Comp_file function that fetches templates
    rates_analysis = table_script.individual_flatfile(LOB='SG',
        URRT_folder=templates['URRT'],
        plans_folder=templates['Plans & Benefits Template'],
        rates_folder=templates['Rates Table Template']
    )
    print(rates_analysis.head())



if __name__ == '__main__':
    # Timing the complete operation of pulling data and processing it
    duration = timeit.timeit('rates_analysis_wrapper()', globals=globals(), number=1)

    # Convert duration from seconds to minutes and seconds for easier reading
    minutes = int(duration / 60)
    seconds = int(duration % 60)
    
    print(f"To complete the rates analysis table creation, it took {minutes} minutes and {seconds} seconds.")