import os
import pandas as pd
import time

def get_filepaths_dataframe(directory, Ignore=None,give_second_dupreomved_df=False, multiple_or_no_dot_handler=True, find_dicom=False):
    """
    List all files in a directory (file name, file extension, folder direcotry, to_file directory) while optionally ignoring specific file extensions.
    It also checks for validity of dicom files, since some dicom files don't have any extension (they usualy have .dcm, however).
    
    
    Args:
        directory (str): The path to the directory to search for files.
        Ignore (list, optional): A list of file extensions to ignore. If specified, files with these extensions
        will be excluded from the list. Default is None.
        give_second_dupreomved_df (bool, optional): If True, a second DataFrame is generated with duplicated file formats
        within one directory and their count in the data directory.
        multiple_or_no_dot_handler (bool, optional): If True, it will handle the file names with multiple dots, 
        or files that have no format (e.g ".dcm)")

    Returns:
        pandas.DataFrame: A DataFrame with columns 'Full_Directory' and 'File' containing file information.

    If `give_second_dupreomved_df` is set to True, the function returns a tuple of two DataFrames:
    1. The first DataFrame contains all file information, including the file's full directory, file name, and file format.
    2. The second DataFrame (only if `give_second_dupreomved_df` is True) contains the same file information but with
       duplicated file formats within a directory removed, along with a count of each file format in the directory.
    
    If `find_dicom` is set to True, the function returns a tuple of two DataFrames, including a column checking for dicom format of each file:
    
    
    The function also measures the execution time and prints it to the console.

    Example:
        directory_path = r'/path/to/directory'
        Ignore = [".dcm"]  # List of file extensions to ignore
        data, count_perDirectandType = get_filepaths_dataframe(directory_path, Ignore, give_second_dupreomved_df=True, multiple_or_no_dot_handler=True,find_dicom=False)
        print(data)  # Display all files
        print(count_perDirectandType)  # Display files with duplicated formats removed and counts.
    """
    try:
        import os
        import pandas as pd
        import time
        if find_dicom==True:
            import pydicom
    except ImportError:
        raise ImportError("The required packages (os, pandas, time. Or pydicom if you set check dicom as true) are not imported. Please make sure to import these packages before using this function.")
    start_time=time.time()

    if find_dicom is True:
        data = {'File': [], 'Full_Directory': [], 'If_dicom':[]}
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1]
                if Ignore and file_extension in Ignore:
                    continue  # Skip files with extensions specified in the Ignore list
                
                data['Full_Directory'].append(root)
                data['File'].append(file)
                data['If_dicom'].append(pydicom.misc.is_dicom(file_path))

        
        tmp_data=pd.DataFrame(data)     
        data_split=tmp_data['Full_Directory'].str.split('\\\\', expand=True)
        data_split.columns = [f'Sub_dir_{i+1}' for i in range(data_split.shape[1])]
        data=pd.concat([tmp_data, data_split], axis=1)

        if multiple_or_no_dot_handler == True:
            data['File_Format'] = data['File'].apply(lambda x: x.rsplit('.', 1)[-1] if '.' in x else 'WARNING: NODATAFORMAT')
        else:
            data['File_Format'] = data['File'].str.split('.').str[-1]

        if give_second_dupreomved_df==True:
            count = data.groupby(['Full_Directory', 'File_Format','If_dicom'])['File_Format'].count().reset_index(name='Count')    
            cdata_split=count['Full_Directory'].str.split('\\\\', expand=True)
            cdata_split.columns = [f'Sub_dir_{i+1}' for i in range(cdata_split.shape[1])]
            count_perDirectandType=pd.concat([count, cdata_split], axis=1)


        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time} seconds")
        

        if give_second_dupreomved_df == True:
            return data, count_perDirectandType
            print("since you turned give_second_dupreomved_df on, this function will give you two dataframes (dupremoved with counts as the second df)")
        else:
            return data
        


    else:
        data = {'File': [], 'Full_Directory': []         
                ,'to_file':[], 'If_dicom':[]}
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1]
                if Ignore and file_extension in Ignore:
                    continue  # Skip files with extensions specified in the Ignore list
                
                data['Full_Directory'].append(root)
                data['File'].append(file)
                data['If_dicom'].append(pydicom.misc.is_dicom(file_path))

        
        tmp_data=pd.DataFrame(data)     
        data_split=tmp_data['Full_Directory'].str.split('\\\\', expand=True)
        data_split.columns = [f'Sub_dir_{i+1}' for i in range(data_split.shape[1])]
        data=pd.concat([tmp_data, data_split], axis=1)

        if multiple_or_no_dot_handler == True:
            data['File_Format'] = data['File'].apply(lambda x: x.rsplit('.', 1)[-1] if '.' in x else 'WARNING: NODATAFORMAT')
        else:
            data['File_Format'] = data['File'].str.split('.').str[-1]

        if give_second_dupreomved_df==True:
            count = data.groupby(['Full_Directory', 'File_Format'])['File_Format'].count().reset_index(name='Count')    
            cdata_split=count['Full_Directory'].str.split('\\\\', expand=True)
            cdata_split.columns = [f'Sub_dir_{i+1}' for i in range(cdata_split.shape[1])]
            count_perDirectandType=pd.concat([count, cdata_split], axis=1)


        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time} seconds")
        

        if give_second_dupreomved_df == True:
            return data, count_perDirectandType
            print("since you turned give_second_dupreomved_df on, this function will give you two dataframes (dupremoved with counts as the second df)")
        else:
            return data


### F O R    D E B U G"""""
Hospital_name= "Guilan"
directory=f"D:\Data\Big Pancreas (CT, EUS)\Raw Data Hospital\{Hospital_name}"

Ignore=None
give_second_dupreomved_df=True
multiple_or_no_dot_handler=True
find_dicom=True
import os
import pandas as pd
import time
import pydicom

start_time=time.time()

data = {'File': [], 'Full_Directory': [],'If_dicom':[]}

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        file_extension = os.path.splitext(file)[1]
        
        if Ignore and file_extension in Ignore:
            continue  # Skip files with extensions specified in the Ignore list
        
        data['Full_Directory'].append(root)
        data['File'].append(file)
        data['If_dicom'].append(pydicom.misc.is_dicom(file_path))


tmp_data=pd.DataFrame(data)     
data_split=tmp_data['Full_Directory'].str.split('\\\\', expand=True)
data_split.columns = [f'Sub_dir_{i+1}' for i in range(data_split.shape[1])]
data=pd.concat([tmp_data, data_split], axis=1)

if multiple_or_no_dot_handler == True:
    data['File_Format'] = data['File'].apply(lambda x: x.rsplit('.', 1)[-1] if '.' in x else 'WARNING: NODATAFORMAT')
else:
    data['File_Format'] = data['File'].str.split('.').str[-1]

if give_second_dupreomved_df==True:
    count_perDirectandType = data.groupby(['Full_Directory', 'File_Format'])['File_Format'].count().reset_index(name='Count')

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time} seconds")