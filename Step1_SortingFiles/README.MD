
### STEP 1 BIG PICTURE
We collected data from centers in folders, named as patient ID (e.g. admission). We want to clean these directories, so 
I: Each CT study is placed in one folder
II: Store cases in an excel file, with its dicom files in the table, and all other variables (outcome, clinical, pathology data) stored here. We call this master key, which also contains patient id (un-anonymized) along with the key for anonymization.
III: Transfer dicom-pnly files to new destination and anonymize these images.

**I created a .py file for re-use in command line**
#### HOW TO USE
This code is prepared on windows 11 system. 
###### 1. Open command on windows
Open your command line (if you don't know how, [see this](https://www.digitalcitizen.life/open-cmd/) )
###### 2. Installing Python
Ensure that you installed python (if this is your first time, I recommend installing anaconda, which also contains many other required python packages. (See this for isntalling anaconda)(https://docs.anaconda.com/free/anaconda/install/windows/))
###### 3. Download my code
I placed all codes in step 1 in one python file named 1_all_in_one_for_reuse.py. You should donwload this, and then you should know the path to this file. The path to file is something like this C:\User\Legion\Documents\PanCanAID\1_all_in_one_for_reuse.py
###### 4. run the python file
write this in your command line: python {path to downloaded file}. For example you should write
    python C:\User\Legion\Documents\PanCanAID\1_all_in_one_for_reuse.py

###### 5. Interact with me :)
In each step I will aks you some information and options, and I will provide next steps. DOn't worry, just follow the text show in command line. Let me know of any issue at sdamirsa@gmail.com
