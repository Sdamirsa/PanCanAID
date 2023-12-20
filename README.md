# What is [PanCanAID](http://pancanaid.com/)
An artificial intelligence model and associated data bank of CT scan, EUS, and survival of pathologically confirmed pancreas cancer (Pancreas ductal adenocarcinoma and pancreas neuroendocrine tumors) will be collected from seven medical centres. Annotation and manual segmentation will be handled by an expert reviewer and confirmed by a second investigator.

# A Code for you (RE-USE): extracting dicom meta, assigning pseudonymized number, renaming folders, and anonymizing dicom

I prepared a no-code Python script that you can run from the command line. [Please go to the folder named Step1_SortingFiles for a detailed guide.](https://github.com/Sdamirsa/PanCanAID/blob/main/Step1_SortingFiles)

It will guide you step by step to:
1- extract the dicom meta and store it in an Excel and JSON file
2- Assing desired pseudonymized numbers to folder names, and then add this code to the previously created Excel file (optional)
3- It will comprehensively anonymize dicom metadata (just necessary dicom meta will be remained), and assign folder name as patient name and id.

That's it. Remember that for using it you should locate each dicom study (which can contain many files and series) in one folder in your directory.
However, it can identify dicom studies even located in one folder of the directory (I am using study_id, study_date, and folder name to find unique studies). I wish you all luck in your projects, and since I was almost dead while handling so many tasks from so many centres I created this code for you and myself :) cheers

# Project Steps
<details>
<summary>STEP 1: SORTING_Transfer_ANONYMIZATION<</summary>
We collected data from centres in folders, named as patient ID (e.g. admission). We want to clean these directories, so 
I: Each CT study is placed in one folder
II: Store cases in an excel file, with its dicom files in the table, and all other variables (outcome, clinical, pathology data) stored here. We call this master key, which also contains the patient id (un-anonymized) along with the key for anonymization.
III: Transfer dicom-pnly files to new destination and anonymize these images.
</details>

<details>
<summary>STEP 2: Labeling\SEGMENTATION XNAT SERVER</summary>
In this step we will use XNAT-Desktop Client to upload dicom files, and then we will download the segmentation from the server we created for our own project using open-source XNAT. 11 Radiologist will accepted our request, all of them had a minimum of 5 year of experince.

Also, we asked 4 general practitioners to label our phases, since the series descriptions are not valid among many centers involved in our study.
</details>

> I tried to add a heading 'changables', which contain all variables, direcotry, etc, that user should define to reuse this code. I hope it can help you on your project : )



## MY TO DO
<details>
<summary>Data Collection from centers: </summary>
- [ ] T
- [ ] Ek
- [ ] G
- [ ] F
- [ ] S
- [ ] B
- [ ] Eh
- [ ] R
- [ ] Y
</details>

<details>
<summary>List of all CTs: </summary>
- [ ] T
- [ ] Ek
- [ ] G
- [ ] F
- [ ] S
- [ ] B
- [ ] Eh
- [ ] R
- [ ] Y
</details>

<details>
<summary>Validation (report or patho or physian or chemo/surgery):</summary>
- [ ] T
- [ ] Ek
- [ ] G
- [ ] F
- [ ] S
- [ ] B
- [ ] Eh
- [ ] R
- [ ] Y
</details>

<details>
<summary>Master Key Completion:</summary>
- [ ] T
- [ ] Ek
- [ ] G
- [ ] F
- [ ] S
- [ ] B
- [ ] Eh
- [ ] R
- [ ] Y
</details>


<details>
<summary>Anonymize and Server:</summary>
- [ ] T
- [ ] Ek
- [ ] G
- [ ] F
- [ ] S
- [ ] B
- [ ] Eh
- [ ] R
- [ ] Y
</details>

<details>
<summary>Follow-up calls</summary>
- [ ] T
- [ ] Ek
- [ ] G
- [ ] F
- [ ] S
- [ ] B
- [ ] Eh
- [ ] R
- [ ] Y
</details>
