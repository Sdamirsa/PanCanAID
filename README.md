# What is PanCanAID
An artificial intelligence model and associated data bank of CT scan, EUS, and survival of pathologically confirmed pancreas cancer (Pancreas ductal adenocarcinoma and pancreas neuroendocrine tumors) will be collected from seven medical centers. Annotation and manual segmentation will be handled by an expert reviewer and confirmed by a second investigator.

# Project Steps
<details>
<summary>STEP 1: SORTING_Transfer_ANONYMIZATION<</summary>
We collected data from centers in folders, named as patient ID (e.g. admission). We want to clean these directories, so 
I: Each CT study is placed in one folder
II: Store cases in an excel file, with its dicom files in the table, and all other variables (outcome, clinical, pathology data) stored here. We call this master key, which also contains patient id (un-anonymized) along with the key for anonymization.
III: Transfer dicom-pnly files to new destination and anonymize these images.
</details>

<details>
<summary>STEP 2: Labeling\SEGMENTATION XNAT SERVER</summary>
In this step we will use XNAT-Desktop Client to upload dicom files, and then we will download the segmentation from the server we created for our own project using open-source XNAT. 11 Radiologist will accepted our request, all of them had a minimum of 5 year of experince.

Also, we asked 4 general practitioners to label our phases, since the series descriptions are not valid among many centers involved in our study.
</details>

    I tried to add a heading 'changables', which contain all variables, direcotry, etc, that user should define to reuse this code. I hope it can help you on your project : )



## MY TO DO
<details>
<summary>Data Collection from centers: </summary>
- [] T
- [] Ek
- [] G
- [] F
- [] S
- [] B
- [] Eh
- [] R
- [] Y
</details>

<details>
<summary>List of all CTs: </summary>
- [] T
- [] Ek
- [] G
- [] F
- [] S
- [] B
- [] Eh
- [] R
- [] Y
</details>

<details>
<summary>Validation (report or patho or physian or chemo/surgery):</summary>
- [] T
- [] Ek
- [] G
- [] F
- [] S
- [] B
- [] Eh
- [] R
- [] Y
</details>

<details>
<summary>Master Key Completion:</summary>
- [] T
- [] Ek
- [] G
- [] F
- [] S
- [] B
- [] Eh
- [] R
- [] Y
</details>


<details>
<summary>Anonymize and Server:</summary>
- [] T
- [] Ek
- [] G
- [] F
- [] S
- [] B
- [] Eh
- [] R
- [] Y
</details>

<details>
<summary>Follow-up calls</summary>
- [] T
- [] Ek
- [] G
- [] F
- [] S
- [] B
- [] Eh
- [] R
- [] Y
</details>
