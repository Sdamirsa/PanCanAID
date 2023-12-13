What is PanCanAID
An artificial intelligence model and associated data bank of CT scan, EUS, and survival of pathologically confirmed pancreas cancer (Pancreas ductal adenocarcinoma and pancreas neuroendocrine tumors) will be collected from seven medical centers. Annotation and manual segmentation will be handled by an expert reviewer and confirmed by a second investigator.

<details>
<summary>STEP 1: DATA SORTING-CLEANING-ANONYMIZATION<</summary>
We collected data from centers in folders, named as patient ID (e.g. admission). We want to clean these directories, so 
I: Each CT study is placed in one folder
II: Store cases in an excel file, with its dicom files in the table, and all other variables (outcome, clinical, pathology data) stored here. We call this master key, which also contains patient id (un-anonymized) along with the key for anonymization.
III: Transfer dicom-pnly files to new destination and anonymize these images.
</details>

<details>
<summary>STEP 2: SEGMENTATION XNAT SERVER</summary>
In this step we will use XNAT-Desktop Client to upload dicom files, and then we will download the segmentation from the server we created for our own project using open-source XNAT.
</details>

    I tried to add a heading 'changables', which contain all variables, direcotry, etc, that user should define to reuse this code. I hope it can help you on your project : )
    
