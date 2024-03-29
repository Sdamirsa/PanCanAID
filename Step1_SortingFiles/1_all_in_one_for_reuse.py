#to do: add 'folder renaming' from the dictionary 
#to do: add Getting user input from one command or pop up winwod (ITK for example)

import pkg_resources
import sys
import subprocess





### P1 packages and environment -------------------------------------------------

### P1 ### P1.1 Ask user for correct formating of direcotry ----------------------------------
check_formating=input('''----------------------- \n Are you sure that you placed each dicom studies within one folder in your direcotry? 
                      You need to give the direcotry of your main folder that contains subfolders, each containing dicom study files
                      You can have other file types, dicom files without extension. Also, our code can find unique dicom studies, even if you locate 
                      them in the same subfolde, but my recommendation is to avoid doring this. Here is the example of direcotry tree:
                      Main Direcotry
                        |
                        |___DicomStudy1
                        |_________SR1
                        |_________________0001.dcm
                        |_________________0002.dcm
                        |_________SR2
                        |_________________0001.dcm
                        |_________________0002.dcm
                        |
                        |___DicomStudy2
                        |________S0001.dcm
                        |________S0002.dcm
                        
                        ----------------------- \n
                      Enter 'y' to confirm this structure and continue \n ''')

check_formating_confirm_list=['y', 'Y', 'yes']
check_formating_confirm_list=['y', 'Y', 'yes']
if check_formating not in check_formating_confirm_list:
    print("See you after restructuring your folders. Exiting script.")
    sys.exit()
    
### P1 ### P1.2 Checking the required packages ------------------------------------------------
print('I will check that if requried packages are installed or not.')
required_packages = {
    "pydicom": "pydicom",
    "tqdm": "tqdm",
    "pandas": "pandas",
    "openpyxl": "openpyxl", # for writing Excel files
    "IPython": "ipython",
    "uuid": "", # part of the standard library
    "shutil": "", # part of the standard library
    "dicognito": "dicognito", 
    "colorama": "colorama" # for colors
}

def check_packages():
    missing_packages = []

    for package, import_name in required_packages.items():
        if import_name:  # Skip standard library packages
            try:
                pkg_resources.require(import_name)
            except pkg_resources.DistributionNotFound:
                missing_packages.append(package)
            except pkg_resources.VersionConflict as e:
                print(f"Version conflict for {package}: {e}. Please update the package.")
            else:
                print(f"{package} is already installed.")

    return missing_packages

missing_packages = check_packages()

if missing_packages:
    print("\nThe following packages are not installed:")
    for package in missing_packages:
        print(f"- {package}")

    print("\nPlease install the missing packages using the following command:")
    print(f"pip install {' '.join(missing_packages)}")
else:
    print("All required packages are installed.")
    no_missing_packages=True ### PROBLEM



### P1 ### P1.3 Force install or exist ----------------------------------------------------
if no_missing_packages is False:
    force_instal=input('''----------------------- \n do you want me to install these packages myself? 
                    I can do it forcefully, but it would be better to install it by the previous command I provided.
                    If you want me to do it enter 'force' otherwise, run me again when you are fiished installing the packages. \n ''')

    force_instal_confirm_list=['Force', 'force','forc','Forc']

    if force_instal in force_instal_confirm_list:
        def install(package):
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        for package, import_name in required_packages.items():
            try:
                pkg_resources.require(import_name)
            except pkg_resources.DistributionNotFound:
                print(f"Installing {package}...")
                install(package)
            except pkg_resources.VersionConflict as e:
                print(f"Version conflict for {package}: {e}")
                # Handle the conflict or prompt user for action
            else:
                print(f"{package} is already installed.")

        print("All required packages are installed.")
    else:
        print('See you after, you installing the packages. Again, I printed the required command line code for you below. Exiting script.')
        print("\nPlease install the missing packages using the following command:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit()

### P1 ### P1.4 importing ----------------------------------------------------------
import pydicom as pm #for reading dicoms
import os #for looping through system direcotries
from pydicom.multival import MultiValue #for reading dicom metadata
from pydicom.valuerep import PersonName #since tunring dictionary to json raised an error you should use this
from tqdm import tqdm #for that fancy loop progress, I like it though
import pandas as pd #for tunring dic to excel, first we trasnform it to pandas dataframe
import json #for storing as json
import shutil #for transfering files (copy, cut, paste)
import dicognito.anonymizer #for anonymizing dicoms
import colorama # for colors in cmd
from colorama import Fore, Style # for colors in cmd
colorama.init()

### P2 Direcotry and Pipiline Options
### P2 ### P2.1 Ask for the main direcotries and namings -----------------------------------

dicom_dir = None
while dicom_dir is None:
    dicom_dir_user = input(Fore.BLUE+'''----------------------- \n Please give me the exact address of your main directory (without quotation). 
                           For example "C:\\PanCanAID_Valid_Case_20231212": \n '''+ Fore.RESET)
    
    if os.path.exists(dicom_dir_user):
        print("Directory found. Press enter to continue.")
        dicom_dir = dicom_dir_user
    else:
        print("Directory does not exist. Please try again.")
        
        

### P2 ### P2.2 Ask for the dicom meta direcotry and if they want pseudonymizaion -----------
def count_subfolders(directory):
    '''this will cont the number of files and folders within a direcotyr'''
    total_subfolders = 0
    total_files=0
    for root, dirs, files in os.walk(directory):
        total_subfolders += len(dirs)
        total_files += len(files)
    return total_subfolders,total_files 
dicom_dir_folder_count,dicom_dir_file_count=count_subfolders(dicom_dir)

dicommeta_and_psudo_user = None

while dicommeta_and_psudo_user is None:
        
    dicommeta_and_psudo_user = input(Fore.BLUE+f'''----------------------- \n you have {dicom_dir_folder_count} folders and total of {dicom_dir_file_count} files.
        Now I want to store these dicom studies, along with their series information in a json and excel file.
        This code will loop through all files, identify unique dicom studies (even if they are located in one sub folder, which is a bad practice).
        Then it will store study information, patient information, and series information. Each dicom study may have multiple dicom series.
        
        After that, we can rename all folders to numbers. The folder number will be used in the next stages for the anonymization 
        (we will remove patient information and use folder names as patient ids). The whole process is commonly known as pseudonymization. 
        If you want me to do this, I will add a column to your excel called 'pseudonymized_id' 
        so you can retrieve information of each case for future use, while the cases are fully anonymized. 
        ----------------------- \n
        If you want me to STORE DICOM META DATA IN EXCEL AND JSON ONLY, say: 'meta only'
        If you want me to STORE DICOM META DATA AND ASSIGN FOLDER NUMBERS, say: 'meta with pseudo' \n \n 
        If you want me to SKIP THIS PHASE, say: 'skip'
        '''+ Fore.RESET)

    dicommeta_and_psudo_user_metaonly = ['meta only', 'Meta Only', 'metaonly', 'Meta only']
    dicommeta_and_psudo_user_metawpseudo = ['meta with pseudo', 'Meta with pseudo', 'meta w pseudo', 'metawithpseudo', 'Meta with Pseudo', 
                                            'meta with psudo', 'meta with psedo', 'meta with psoudo', 'meta with pseodu', 'meta with psdo']

    if dicommeta_and_psudo_user in dicommeta_and_psudo_user_metaonly:
        dicommeta_and_psudo_user = 'meta only'
        print('You chose to store dicom meta only.')
        
    elif dicommeta_and_psudo_user in dicommeta_and_psudo_user_metawpseudo:
        while True:
            pseuo_start_number = input(Fore.BLUE+'''----------------------- \n Please give me your starting number with at least 4 digits. I will use this to rename your folders.
                                    For example, if you give me 3000, I will name folders as 1000, 1001, 1002, ...
                                    Note that your folder names should be unique from your previous ones (if you have any) so you can have one
                                    pseudonymized number for each DICOM study. If a patient has two DICOMs, you should have two numbers for each study: \n \n '''+ Fore.RESET)

            if pseuo_start_number.isdigit() and len(pseuo_start_number) > 3:
                pseuo_start_number = int(pseuo_start_number)  # Convert to integer if validation is successful
                break
            else:
                print("Invalid input. Please enter a four-digit number.")
        pseuo_start_beginingtext = input(Fore.BLUE+'''----------------------- \n if you want me to add some string (text) at the beginning of your folder names, give it to me here.
                        For example, if you give me 'Case', I will rename folders as: Case_1001, Case_1002, ....
                        Leave blank if you don't want it. \n \n'''+ Fore.RESET)
        if len(pseuo_start_beginingtext) > 0:
            pseuo_start_beginingtext = str(pseuo_start_beginingtext) + '_'
            
        dicommeta_and_psudo_user = f'meta with pseudo starting at {pseuo_start_beginingtext}{pseuo_start_number}'
        print(f'You chose to store dicom meta and then change folder names to pseudonymized numbers starting at {pseuo_start_beginingtext}{pseuo_start_number}.')
            
    elif dicommeta_and_psudo_user == 'skip':
        print('You chose to skip storing dicom meta data.')
    else:
        print("Invalid input. Please try again.")
        dicommeta_and_psudo_user = None     


        
        
justpass=input(Fore.BLUE+'''----------------------- \n please make sure that you close all open files that are located in your directory, 
      and press any key afer you closed all open files '''+ Fore.RESET)


### P3 ### P3.1 ### Functions:Extracting dicom meta -----------------------------------------------
# This is the code provided in 1_2_Add_Dicom_Meta_to_Table.ipynb step
    
#FINAL 20231216
#My context: I coded this on my windows11 with RTC3080Ti and Corei9-12gen and 32G Ram. I am coding on VS code and using jupyter notebook.
#Your requirment: It doesn't need any exceptional hardward you can run it on an average pc/labtob

import pydicom as pm #for reading dicoms
import os #for looping through system direcotries
from pydicom.multival import MultiValue #for reading dicom metadata
from pydicom.valuerep import PersonName #since tunring dictionary to json raised an error you should use this
from tqdm import tqdm #for that fancy loop progress, I like it though
import pandas as pd #for tunring dic to excel, first we trasnform it to pandas dataframe
import json #for storing as json


def get_dicom_tag_value(dicom_file, tag, default=None):
    '''this function will get the dicom tag from the dicom filde for the given tag/code'''
    tag_value = dicom_file.get(tag, None)
    if tag_value is None:
        return default
    if isinstance(tag_value, MultiValue):
        return list(tag_value)  # Convert MultiValue to list
    return tag_value.value

def get_path_to_first_subfolder(full_path, first_subfolder):
    """this will get the path to the first folder of root, which is the subfolder that contains all dicom filed of one dicom study """
    path_parts = full_path.split(os.sep)
    if first_subfolder in path_parts:
        subfolder_index = path_parts.index(first_subfolder)
        return os.sep.join(path_parts[:subfolder_index + 1])
    else:
        return full_path

def count_subfolders(directory):
    '''this will cont the number of files and folders within a direcotyr'''
    total_subfolders = 0
    total_files=0
    for root, dirs, files in os.walk(directory):
        total_subfolders += len(dirs)
        total_files += len(files)
    return total_subfolders,total_files 


class CustomJSONEncoder(json.JSONEncoder): #this class will turn our multilevel dictionary into a json file
    def default(self, obj):
        if isinstance(obj, MultiValue):
            return list(obj)  # Convert MultiValue to list
        elif isinstance(obj, PersonName):
            return str(obj)   # Convert PersonName to string
        return json.JSONEncoder.default(self, obj)

def ensure_json_extension(directory): 
    '''this function will ensure that definied json direcotry contains the required extension, otherwise, it will add this to the end of definied dir'''
    if not directory.endswith(".json"):
        return directory + "\\DicomMeta_JSON.json"
    return directory

def ensure_excel_extension(directory):
    '''this function will ensure that definied excel direcotry contains the required extension, otherwise, it will add this to the end of definied dir'''
    if not directory.endswith(".xlsx"):
        return directory + "\\DicomMeta_excel.xlsx"
    return directory



def get_dicomdir_give_dicomdicom_datadic(dicom_dir, #direcotry that you want to read, usually dicom studies should be in one folder, preferably with patient unique id/name
                                     dicom_validation=True, #this will check wether the file in the loop is dicom or not. Although make it slower, I recommend using it to ensure only dicom files go through loop 
                                     folder_list_name_indicomdir=None, #In your dicom_dir you can include list of folders name that you want to read. It will not read other folders. Kepp in mind that this will look into subfolders in the main folder, and not the subfolders of subfolders :)
                                     store_as_json_dir=None, #if you want to store your ditionary as json, give your desired json direcotry
                                     store_as_excel_dir=None #if you want to store your ditionary as excel, give your desired excel direcotry
                                     ):
    """
    This function creates a multi-level dictionary for DICOM meta data (named dicom_data) in a directory (named dicom_dir).
    The top level has the last component of dicom_dir, which is the first level subfolder, as a key.
    For each subforled it will store study data within this dic, along with another dicitonary for series data, within this study dictionary.
    For series dictionary the data corresponding for series number will be stored.
    We also have another private_info dictionary within subfodler dictionary.
    
    - dicom_validation: If you set dicom_validation=True, it will validate the file in the loop for being an dicom file. This is super important although it makes code slower.
    Becaouse, sometimes some dicom files have no extension, and also reading other files may cause error in the loop.
    
    - folder_list_name_indicomdir: #In your dicom_dir you can include list of folders name that you want to read. It will not read other folders. Kepp in mind that this will look into subfolders in the main folder, and not the subfolders of subfolders :)
    
    - store_as_json_dir: if you want to store your ditionary as json, give your desired json direcotry
    
    - store_as_excel_dir: if you want to store your ditionary as excel, give your desired excel direcotry
    
    For using this function, the best practice is to place each folder containing one dicom study in subfolder, under the dicom_dir. 
    However, you can change finding unique dicom studies, even placed next to each other beacouse I definied the study_unique=f'{first_subfolder}_{study_id}_{study_date}'.
    If you want your code to be faster you can chane the study_unique to study_unique=first_subfolder. It makes your code 15% faster, sometimes at the cost of incurrect retrival.
    
    """

    total_subfolder,total_files=count_subfolders(dicom_dir)
    print(f'your direcotry contains {total_subfolder} folders and {total_files} files')
    
    last_dir_name = os.path.basename(os.path.normpath(dicom_dir))
    dicom_data = {last_dir_name: {}}

    for root, dirs, files in tqdm(os.walk(dicom_dir), desc="Processing directories", total=total_subfolder,unit='folder'):
        if folder_list_name_indicomdir:
            split_path = root.replace(dicom_dir, '').split(os.sep)
            first_subfolder = split_path[1] if len(split_path) > 1 else ""
            if first_subfolder not in folder_list_name_indicomdir:
                print(f"""The folder {first_subfolder} was not in your definied list.""")
                continue  # Skip if the first subfolder is not in the user-defined list
            
        for file in files:
            if dicom_validation and not pm.misc.is_dicom(os.path.join(root, file)):
                continue # Skip if the it is not dicom file
                   

            try:
                dicom_file = pm.dcmread(os.path.join(root, file))
                study_id = get_dicom_tag_value(dicom_file, (0x0020, 0x0010))
                dicom_data_number = get_dicom_tag_value(dicom_file, (0x0020, 0x0011))
                study_date = get_dicom_tag_value(dicom_file, (0x0008, 0x0020))
                split_path = root.replace(dicom_dir, '').split(os.sep)
                first_subfolder = split_path[1] if len(split_path) > 1 else ""
                if study_id and dicom_data_number and study_date:
                    study_unique = f'{first_subfolder}_{study_id}_{study_date}' #you can change it for increasing the speed > study_unique=first_subfolder
                    if study_unique not in dicom_data[last_dir_name]:
                        private_info={'name': get_dicom_tag_value(dicom_file, (0x0010, 0x0010)),
                                      'institute': get_dicom_tag_value(dicom_file, (0x0008, 0x0080)),
                                      'patient_id': get_dicom_tag_value(dicom_file, (0x0010, 0x0020)),
                                      'accession_number':get_dicom_tag_value(dicom_file, (0x0008, 0x0050))
                                      }
                        
                        dicom_data[last_dir_name][study_unique] = {
                            'dir_to_root': get_path_to_first_subfolder(root, first_subfolder),
                            'study_description': get_dicom_tag_value(dicom_file, (0x0008, 0x1030)),
                            'date': study_date,
                            'age': get_dicom_tag_value(dicom_file, (0x0010, 0x1010)),
                            'sex': get_dicom_tag_value(dicom_file, (0x0010, 0x0040)),
                            'manufacture_model': get_dicom_tag_value(dicom_file, (0x0008, 0x1090)),
                            'manufacture_brand': get_dicom_tag_value(dicom_file, (0x0008, 0x0070)),
                            'manufacture_brand': get_dicom_tag_value(dicom_file, (0x0008, 0x0070)),
                            'protocol': get_dicom_tag_value(dicom_file, (0x0018, 0x1030)),
                            'study_id': study_id,
                            'patient_weight': get_dicom_tag_value(dicom_file, (0x0010, 0x1030)),
                            'Image_type': get_dicom_tag_value(dicom_file, (0x0008, 0x0008)),
                            'body_part': get_dicom_tag_value(dicom_file, (0x0018, 0x0015)),
                            'modalitty':get_dicom_tag_value(dicom_file, (0x0008, 0x0050)),
                            'private_info':private_info,
                            'image_dicom_data_list': {}
                        }

                    

                    dicom_data_info = {
                        'dicom_data_description': get_dicom_tag_value(dicom_file, (0x0008, 0x103E)),
                        'body_part': get_dicom_tag_value(dicom_file, (0x0018, 0x0015)),
                        'slice_thickness': get_dicom_tag_value(dicom_file, (0x0018, 0x0050)),
                        'Image_comment': get_dicom_tag_value(dicom_file, (0x0020, 0x4000)),
                        'kvp': get_dicom_tag_value(dicom_file, (0x0018, 0x0060)),
                        'exposure': get_dicom_tag_value(dicom_file, (0x0018, 0x1152)),
                        'exposure_time': get_dicom_tag_value(dicom_file, (0x0018, 0x1150)),
                    }
                    dicom_data[last_dir_name][study_unique]['image_dicom_data_list'][dicom_data_number] = dicom_data_info

            except Exception as e:
                print(f"""Error reading for {file}::: {e} \n """)
                continue
            
    if store_as_json_dir is not None:
        try:
            json_read = json.dumps(dicom_data, indent=4, cls=CustomJSONEncoder)
            store_as_json_dir=str(store_as_json_dir)
            store_as_json_dir=ensure_json_extension(store_as_json_dir)
            with open(store_as_json_dir, 'w') as json_file:
                json_file.write(json_read)
            print(f"""Json stored at :::""")
            print(Fore.GREEN+store_as_json_dir+Fore.RESET)         
        except:
            print(f"""Error storing the json ::: {e} \n """)
            
    if store_as_excel_dir is not None:
        try:
            dataframes = []
            for key, value in dicom_data.items():
                # Convert value to DataFrame if necessary
                df = pd.DataFrame(value)
                # Add the key as a new column or as part of the index
                df['Key'] = key  # Add key as a column
                # df = df.set_index(['Key'], append=True)  # Add key as part of a MultiIndex
                dataframes.append(df)

            # Concatenate all dataframes
            df2 = pd.concat(dataframes).T
            store_as_excel_dir=str(store_as_excel_dir)
            store_as_excel_dir=ensure_excel_extension(store_as_excel_dir)
            df2.to_excel(store_as_excel_dir)
            print(f"""Excel stored at :::""")
            print(Fore.GREEN+store_as_excel_dir+Fore.RESET)       
        except:
            print(f"""Error storing the excel ::: {e} \n """)
            
                                 
    return dicom_data

### P3 ### P3.1 ### CODE: Extracting dicom meta -----------------------------------------------
print(Fore.YELLOW+'start extracting dicom'+ Fore.RESET)

if dicommeta_and_psudo_user=='meta only':
        
    dicom_dir=dicom_dir #user defined this in section P2.1
    
    dicom_dic=get_dicomdir_give_dicomdicom_datadic(
        dicom_dir, #direcotry that you want to read, usually dicom studies should be in one folder, preferably with patient unique id/name
                                        dicom_validation=True, #this will check wether the file in the loop is dicom or not. Although make it slower, I recommend using it to ensure only dicom files go through loop 
                                        folder_list_name_indicomdir=None, #In your dicom_dir you can include list of folders name that you want to read. It will not read other folders. Kepp in mind that this will look into subfolders in the main folder, and not the subfolders of subfolders :)
                                        store_as_json_dir=dicom_dir, #if you want to store your ditionary as json, give your desired json direcotry
                                        store_as_excel_dir=dicom_dir #if you want to store your ditionary as excel, give your desired excel direcotry
                                        )


### P3 ### P3.2 Extracting dicom meta &&& Renaming folders &&& Storing pseudonymized name in excel ----------

if dicommeta_and_psudo_user=='meta with pseudo':
    
    dicom_dir=dicom_dir #user defined this in section P2.1
    
    dicom_dic=get_dicomdir_give_dicomdicom_datadic(
        dicom_dir, #direcotry that you want to read, usually dicom studies should be in one folder, preferably with patient unique id/name
                                        dicom_validation=True, #this will check wether the file in the loop is dicom or not. Although make it slower, I recommend using it to ensure only dicom files go through loop 
                                        folder_list_name_indicomdir=None, #In your dicom_dir you can include list of folders name that you want to read. It will not read other folders. Kepp in mind that this will look into subfolders in the main folder, and not the subfolders of subfolders :)
                                        store_as_json_dir=dicom_dir, #if you want to store your ditionary as json, give your desired json direcotry
                                        store_as_excel_dir=dicom_dir #if you want to store your ditionary as excel, give your desired excel direcotry
                                        )
    
    print(Fore.YELLOW+'start renaming the folders and adding it to the corresponding previous folder name in excel'+ Fore.RESET)
    #renaming folders and adding pseudonumized number to 
    folder_mapping = {}
    # Iterate through each folder in the directory
    for folder_name in tqdm(os.listdir(dicom_dir), desc='renaming folders'):
        if os.path.isdir(os.path.join(dicom_dir, folder_name)):
            original_folder_path = os.path.join(dicom_dir, folder_name)
            new_folder_name = f"{pseuo_start_beginingtext}{pseuo_start_number}"
            new_folder_path = os.path.join(dicom_dir, new_folder_name)
            

            # Rename the folder
            os.rename(original_folder_path, new_folder_path)

            # Store the mapping
            folder_mapping[original_folder_path] = new_folder_name
            
            pseuo_start_number=pseuo_start_number+1

    # Output the dictionary containing the mappings
    print('the folder mapping is: ')
    print(folder_mapping)

    ##ss
    
    #adding folder mapping to previously stored excel
    excel_dir=ensure_excel_extension(dicom_dir)
    dicommeta_excel_df = pd.read_excel(excel_dir)
    dicommeta_excel_df['dir_to_root']
    dicommeta_excel_df['pseudonymize_code'] = dicommeta_excel_df['dir_to_root'].map(folder_mapping)
    pseudo_excel_file_name = "DicomMeta_with_pseudocode_excel.xlsx"
    pseudo_excel_output_path = os.path.join(dicom_dir, pseudo_excel_file_name)
    dicommeta_excel_df.to_excel(pseudo_excel_output_path, index=False)
    print(f"DataFrame with pseudonymized code saved to :::")
    print(Fore.GREEN+ pseudo_excel_output_path+Fore.RESET)
    

### P4 ### P4.1 Preparing files for Anonymization ----------
#v2
import os
from tqdm import tqdm
from IPython.display import HTML
import pydicom as pm
import shutil


def create_clickable_dir_path(dir_path):
    # Convert the directory path to a file URL
    file_url = f"{dir_path}"
    return HTML(f'<a href="{file_url}" target="_blank">{dir_path}</a>')


def add_series_2beginingoffile(directory, adding_directory_2progresbar=''):
    renamed_count = 0
    skipped_count = 0
    for filename in tqdm(os.listdir(directory), desc=f'Adding series name {adding_directory_2progresbar} at the beginning of files', unit='folders'):
        file_path = os.path.join(directory, filename)

        # Check if it's a file and has a DICOM extension (optional)
        if os.path.isfile(file_path) and pm.misc.is_dicom(file_path):
            try:
                # Read the DICOM file
                dicom_file = pm.dcmread(file_path)

                # Get the series number if it exists
                if hasattr(dicom_file, 'SeriesNumber'):
                    series_number = dicom_file.SeriesNumber
                else:
                    series_number = ''

                # Check if the original file name already contains "SR"
                if filename.startswith('SR'):
                    new_filename = f"{series_number}_{filename}"
                else:
                    new_filename = f"SR{series_number}_{filename}"

                new_file_path = os.path.join(directory, new_filename)

                # Rename (replace) the file if the new file name does not exist
                if not os.path.exists(new_file_path):
                    os.rename(file_path, new_file_path)
                    renamed_count += 1
                else:
                    skipped_count += 1

            except Exception as e:
                skipped_count += 1
                print(f"Error processing {file_path}: {e}")

    print(f"Total files skipped: {skipped_count}")
    print(f"Total files renamed: {renamed_count}")


def add_subfolder_name_and_move(main_directory, adding_directory_2progresbar=''):
    files_moved = 0  # Initialize a counter for the number of files moved

    for folder in tqdm(os.listdir(main_directory), desc=f'Move and rename data from subfolders of {adding_directory_2progresbar}', unit='folders'):
        folder_path = os.path.join(main_directory, folder)

        # Check if it's a directory
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)

                # Check if it's a file
                if os.path.isfile(file_path):
                    # Create new file name with subfolder prefix
                    new_filename = f"{folder}_{file}"
                    new_file_path = os.path.join(main_directory, new_filename)

                    # Move and rename file if the new file name does not exist
                    if not os.path.exists(new_file_path):
                        shutil.move(file_path, new_file_path)
                        files_moved += 1  # Increment the counter
                    else:
                        print(f"File {new_file_path} already exists. Skipping...")

    # Print the total number of files moved
    print(f"Total number of files moved: {files_moved}")

    # Remove empty subfolders
    empty_folder_removed = 0
    for folder in os.listdir(main_directory):
        folder_path = os.path.join(main_directory, folder)

        # Check if the folder is empty and a directory
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)
            empty_folder_removed += 1
            print(f"Removed empty folder: {folder_path}")

    remaining_folders = sum(os.path.isdir(os.path.join(main_directory, d)) for d in os.listdir(main_directory))

    print(f"Number of empty folders removed: {empty_folder_removed}")
    print(f"Number of remaining folders: {remaining_folders}")


def folderedstudy_and_addingseriesname_handler(main_directory):
    for folder in tqdm(os.listdir(main_directory), desc='Reading folders within directory', unit='files'):
        folder_path = os.path.join(main_directory, folder)

        if os.path.isdir(folder_path):
            subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
            count_subfolders = len(subfolders)
            if count_subfolders > 0:
                print(f"#{count_subfolders} Subfolders within: ")
                display(create_clickable_dir_path(folder_path))
                add_subfolder_name_and_move(folder_path, adding_directory_2progresbar=folder_path)
                add_series_2beginingoffile(folder_path, adding_directory_2progresbar=folder_path)
            else:
                print(f"No subfolder exists in:")
                display(create_clickable_dir_path(folder_path))
                add_series_2beginingoffile(folder_path, adding_directory_2progresbar=folder_path)

        print('-----------------------------------------')

### P4 ### P4.2 Anonymizing Dicoms ----------

clean_to_path = None

while clean_to_path is None:
    clean_to_path_user = input(Fore.BLUE + '''----------------------- \n I want to start anonymizing your files. Please give me the exact location that you want to transfer your anonymized
                               dicom files (without quotation): For example C:\\PanCanAID_Valid_Case_Example_cleaned \n ''' + Fore.RESET)

    if os.path.exists(clean_to_path_user):
        print("Directory found.")
        clean_to_path = clean_to_path_user
    else:
        try:
            os.makedirs(clean_to_path_user)
            clean_to_path = clean_to_path_user
            print(f"Directory not found. Directory created at {clean_to_path}.")
        except OSError as e:
            print(f"Directory does not exist and cannot be created. Error: {e}. Please try again.")



InstitueName = input(Fore.BLUE+'''----------------------- \n I will assign folder name as patient name and patient id. 
                           Please define your desired text for institute, for example PanCanAID Project \n'''+ Fore.RESET)
    

print(Fore.YELLOW+'start anononymizing and updating and transfering dicoms'+ Fore.RESET)
import pydicom as pm
import dicognito.anonymizer
from tqdm import tqdm
import os


def Anonymize_and_update_dicom_metadata(dicom_from_path, clean_to_path, InstituteName='InstituteName'):
    anonymizer = dicognito.anonymizer.Anonymizer()
    errors = {}
    for folder_name in tqdm(os.listdir(dicom_from_path), desc='reading directory'):
        folder_input_path = os.path.join(dicom_from_path, folder_name)
        if os.path.isdir(folder_input_path):
            folder_output_path = os.path.join(clean_to_path, folder_name)
            os.makedirs(folder_output_path, exist_ok=True)
            for file in tqdm(os.listdir(folder_input_path), desc=f'anonymizing dicom from {folder_input_path}  to  {folder_output_path}'):
                input_file_path = os.path.join(folder_input_path, file)
                if pm.misc.is_dicom(input_file_path):
                    try:
                        dataset = pm.dcmread(input_file_path)

                        if hasattr(dataset, 'remove_private_tags'):
                            dataset.remove_private_tags()

                        if 'OtherPatientIDs' in dataset:
                            if dataset.OtherPatientIDs.value != '':
                                del dataset.OtherPatientIDs

                        anonymizer.anonymize(dataset)

                        if 'PatientID' in dataset:
                            dataset.PatientID = folder_name
                        if 'PatientName' in dataset:
                            dataset.PatientName = folder_name
                        if 'InstitutionName' in dataset:
                            dataset.InstitutionName = InstituteName
                        if 'InstitutionAddress' in dataset:
                            dataset.InstitutionAddress = InstituteName

                        # Save the modified file
                        dataset.save_as(os.path.join(folder_output_path, "ancl_" + file))
                    except Exception as e:
                        print(f"Error processing {folder_output_path, input_file_path}: {e}")
                        errors[input_file_path] = str(e)+'\n'
    print("Errors encountered: \n", errors)





dicom_from_path = dicom_dir #previously defined by user
clean_to_path = clean_to_path
InstituteName = InstitueName #previously defined by user
print(Fore.YELLOW+f'START: Preparing files in {dicom_from_path} for anonymizasion'+Fore.RESET)
folderedstudy_and_addingseriesname_handler(dicom_from_path)
print(Fore.YELLOW+f'Finish: Preparing files in {dicom_from_path} for anonymizasion'+Fore.RESET)
Anonymize_and_update_dicom_metadata(dicom_from_path=dicom_from_path, clean_to_path=clean_to_path, InstituteName=InstituteName)



print(Fore.GREEN+f'Finished. You can find anonymized and updated dicoms at {clean_to_path}'+ Fore.RESET)
print(Fore.GREEN+'FINISHED, HURAY, Thanks for your patience. You can reach me at sdamirsa@gmail for any inquiry. bye bye.'+ Fore.RESET)