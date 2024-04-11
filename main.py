import pandas as pd
import table_script
import file_pull

['Service Area', 'URRT', 'Rates Table Template', 'Network Template','Plans & Benefits Template']
def Comp_File_Pull():
    template_dict = {}
    for temp in file_pull.files:
        new_folder = file_pull.Rates_File_Puller(type=temp)
        template_dict[temp] = new_folder
    return template_dict

templates = Comp_File_Pull()

rates_analysis = table_script.individual_flatfile(URRT_folder = templates['URRT'],
                        plans_folder = templates['Plans & Benefits Template'],
                        name_mapping_path= r"C:\Users\A654219\Documents\GA\name_mapping.xlsx")


