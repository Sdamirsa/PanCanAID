# PanCanAID 2024 Introduction

In 2024, we upgraded our segmentation pipeline. It now encompasses three primary tasks:

1. PAS (Pancreas Anatomy Segmentation):
   This task focuses on segmenting the pancreas (P), mass (M), main pancreatic duct dilation (MPD), and arteries (AA). We excluded the duodenum segmentation due to the challenges of defining it and the lack of inclusion in our current project's aims.    

2. PDS (Pancreas Diagnostic System):
   This system verifies the PAS results and generates pancreas-related reports. For pancreatic cancer cases, it provides information on metastasis, neural invasion, root of mesentery invasion, staging, and mass characteristics.

3. AAA (Abdominal Anatomy Analysis):
   This task involves segmenting six organs and two vessels within the abdominal cavity: Stomach (G), Liver (L), Gallbladder (GB), Left Kidney (LK), Right Kidney (RK), Spleen (Sp), Inferior Vena Cava (IVC), Aorta (AA)

PanCanAID initially focused on pancreatic cancer, leading to the acquisition of approximately 7,000 CT scans. This extensive dataset spawned a new project, Pars-CT, which aims to develop a foundational model for CT scan analysis. A preprint detailing the design and its corresponding repository will be available soon.

# Mask Guide (Click on the desired task)

This tables guide you on proper segmentation and naming

<details>
<summary> PAS (GP Team) </summary>
  
| Annotator  | Confirm by        | Mask                       | **Mask Name** | If and only if     | Command to annotator                                     | Tool | Est. Req. Time for S. |
| ---------- | ----------------- | -------------------------- | ------------- | ------------------ | -------------------------------------------------------- | ---- | --------------------- |
| Trained GP | Me && Radiologist | Pancreas                   | **P**         | -                  | Around pancreas on all visible axial cut                 | Pen  | 20 m                  |
|            |                   | Deudenum                   | **D**         |                    | Around D1 (from pylori to the end of arm of C shaped D1) | Pen  | 15 min                |
| Trained GP | Me && Radiologist | Mass                       | **M**         | if mass is present | Around pancreas mass on all visible axial cut            | Pen  | 5 m                   |
| Trained GP | Me && Radiologist | MPD                        | **MPD**       | if MPD dilation    | Around MPD in all visible axial cut                      | Pen  | 5 m                   |
| Trained GP | Me && Radiologist | Celiac  & Branche Artery   | **CAB**       |                    | Around Celiac Trunk A. & Common-Hepatic A. & Splenic A.  | Pen  | 10 min                |
| Trained GP | Me && Radiologist | Superior Mesenteric Artery | **SMA**       |                    | Around Superior Mesenteric Artery                        | Pen  | 7 min                 |
| Trained GP | Me && Radiologist | Superior Mesenteric Vein   | **SMV**       |                    | Around Superior Mesenteric Vein                          | Pen  | 7 min                 |
| Trained GP | Me && Radiologist | Portal Vein                | **PV**        |                    | Around Portal Vein                                       | Pen  | 10 min                |

</details>

<details>
<summary> PDS (Radiologist) </summary>
   
0. **Double-check the PAS and provide comments to revise (or revise) the segmentation.**

1. **Mass Characteristics:**
   - Location (head, body, tail, uncinate process)
   - Density (solid, cystic, mixed)
   - Enhancement pattern (hypoenhancing, isoenhancing, hyperenhancing)
   - Margins (well-defined, ill-defined, infiltrative)
   - Presence of calcifications (yes/no)

2. **Metastasis:**
   - Liver metastases (present/absent, number, size of largest)
   - Peritoneal metastases (present/absent)
   - Lung metastases (present/absent)
   - Distant lymph node metastases (present/absent, location)

3. **Local Invasion:**
   - Vascular invasion:
     - Portal vein (present/absent, degree of involvement)
     - Superior mesenteric vein (present/absent, degree of involvement)
     - Celiac axis (present/absent, degree of involvement)
     - Superior mesenteric artery (present/absent, degree of involvement)
     - Common hepatic artery (present/absent, degree of involvement)
   - Adjacent organ invasion:
     - Duodenum (present/absent)
     - Stomach (present/absent)
     - Spleen (present/absent)
     - Left adrenal gland (present/absent)

4. **Resectability (based on provided definition)**:
   - A. Resectable
   - B. Borderline resectable
   - C. Unresectable (locally advanced)
   - D. Unresectable (metastatic disease)
<details>
<summary> Full definition and criteria for Resectability Assessment </summary>

#### *A. Resectable*

- *No distant metastases*
- *No radiographically apparent vascular invasion of:*
  - *Celiac axis (CA)*
  - *Superior mesenteric artery (SMA)*
  - *Common hepatic artery (CHA)*
- *Normal fat plane around CA, SMA, and CHA*
- *Patent superior mesenteric vein (SMV) and portal vein (PV) without signs of tumor invasion or thrombosis*

#### *B. Borderline Resectable*

- *No distant metastases*
- *Venous involvement of SMV/PV with distortion or narrowing of the vein or occlusion of the vein with suitable vessel proximal and distal, allowing for safe resection and reconstruction*
- *Gastroduodenal artery encasement up to the hepatic artery with either short segment encasement or direct abutment of the hepatic artery, without extension to the celiac axis*
- *Tumor abutment of the SMA not to exceed 180 degrees of the circumference of the vessel wall*

#### *C. Locally Advanced (Unresectable)*

- *No distant metastases*
- *Arterial involvement:*
  - *Encasement of > 180 degrees of SMA circumference*
  - *Any CA encasement*
  - *Unreconstructible SMV/PV occlusion*
- *Aortic invasion or encasement*

#### *D. Metastatic Disease (Unresectable)*

- *Presence of distant metastases, including:*
  - *Liver metastases*
  - *Peritoneal metastases*
  - *Lung metastases*
  - *Non-regional lymph node metastases*

#### *Notes for Radiologists:*

1. *Measure the degree of contact between the tumor and major vessels in degrees of circumferential involvement.*
2. *Assess for the presence of a fat plane between the tumor and vessels.*
3. *Look for deformity or narrowing of vessels, especially the SMV and PV.*
4. *Evaluate for the presence of collateral vessels, which may indicate vascular involvement.*
5. *Check for any signs of distant metastases, particularly in the liver, lungs, and peritoneum.*
6. *Consider multiplanar reformations to accurately assess vascular involvement.*

</details>


   
5. **Pancreatic Duct Dilation**:
   - Present/absent
   - Maximum diameter (mm)

6. **Common Bile Duct Dilation**:
   - Present/absent
   - Maximum diameter (mm)

7. **Lymph Node Involvement**:
   - Peripancreatic lymph nodes (present/absent, number, size of largest)
   - Celiac lymph nodes (present/absent, number, size of largest)
   - Para-aortic lymph nodes (present/absent, number, size of largest)

8. **Pancreatic Atrophy**:
   - Present/absent
   - Degree (mild, moderate, severe)

9. **Ancillary Findings**:
   - Pancreatic or biliary stents (present/absent)
   - Ascites (present/absent)
   - Gallstones (present/absent)

</details>

<details>
<summary> AAA (GP/MedS Team) </summary>

| Annotator         | Confirm by        | Mask               | **Name of Mask** | Command to annotator                                                         | Tool | Est. Req. Time for S. |
| ----------------- | ----------------- | ------------------ | ---------------- | ---------------------------------------------------------------------------- | ---- | --------------------- |
| GP/Trained MedStd | Me OR Radiologist | Gastric (Stomache) | **G**            | Around Stomach (outside stomach muscles)                                     | Pen  | 10                    |
| GP/Trained MedStd | Me OR Radiologist | Liver              | **L**            | Around Liver Excluding IVC & main hepatic arteries outside liver             | Pen  | 12                    |
| GP/Trained MedStd | Me OR Radiologist | Gall Bladder       | **GB**           | Around gall bladder                                                          | Pen  | 2                     |
| GP/Trained MedStd | Me OR Radiologist | Left Kidney        | **LK**           | Around left kidney                                                           | Pen  | 7                     |
| GP/Trained MedStd | Radiologist       | Right Kidney       | **RK**           | Around right kidney                                                          | Pen  | 7                     |
| GP/Trained MedStd | Me OR Radiologist | Spleen             | **S**            | Around spleen                                                                | Pen  | 10                    |
| GP/Trained MedStd | Me OR Radiologist | Aorta              | **AA**           | Around aorta, from highest segmented organ to lowest segmented organ (slice) | Pen  | 7                     |
| GP/Trained MedStd | Me OR Radiologist | Inferior Vena Cava | **IVC**          | Around IVC, from highest segmented organ to lowest segmented organ (slice)   | Pen  | 7                     |

</details>


# PanCanAID Guides

Each task has a dedicated Telegram channel providing resources for using our remote segmentation platform and learning abdominal cavity anatomy. To collaborate, please contact me at www.t.me/sdamirsa. Our learning pathways are accessible at www.pancanaid.com/education.

# PanCanAID License

We plan to release the entire dataset (CT scans, clinical data, and segmentations) under a special license. Non-profit use is freely available to researchers, hospitals, and AI companies worldwide. Commercial use requires a 10% allocation of revenue to cancer charities in the country of use. As enforcing this mandate is challenging, we welcome suggestions for commercial users (e.g., a one-time payment to charities every five years).
