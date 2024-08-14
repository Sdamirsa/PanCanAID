# PanCanAID 2024 Introduction

In 2024, we upgraded our segmentation pipeline. It now encompasses three primary tasks:

1. PAS (Pancreas Anatomy Segmentation):
   This task focuses on segmenting the pancreas (P), mass (M), main pancreatic duct dilation (MPD), and arteries (AA).

2. PDS (Pancreas Diagnostic System):
   This system verifies the PAS results and generates pancreas-related reports. For pancreatic cancer cases, it provides information on metastasis, neural invasion, root of mesentery invasion, staging, and mass characteristics.

3. AAA (Abdominal Anatomy Analysis):
   This task involves segmenting six organs and two vessels within the abdominal cavity:
   - Stomach (G)
   - Liver (L)
   - Gallbladder (GB)
   - Left Kidney (LK)
   - Right Kidney (RK)
   - Spleen (S)
   - Inferior Vena Cava (IVC)
   - Aorta (AA)

PanCanAID initially focused on pancreatic cancer, leading to the acquisition of approximately 7,000 CT scans. This extensive dataset spawned a new project, Pars-CT, which aims to develop a foundational model for CT scan analysis. A preprint detailing the design and its corresponding repository will be available soon.

# Mask Guide (Click on desired task)

<detaile>
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

</detaile>

<detaile>
<summary> PDS (Radiologist) </summary>


</detaile>

<detaile>
<summary> PDS (GP/MedS Team) </summary>


</detaile>


This table guides you on proper segmentation and defining names


# PanCanAID Guides

Each task has a dedicated Telegram channel providing resources for using our remote segmentation platform and learning abdominal cavity anatomy. To collaborate, please contact me at www.t.me/sdamirsa. Our learning pathways are accessible at www.pancanaid.com/education.

# PanCanAID License

We plan to release the entire dataset (CT scans, clinical data, and segmentations) under a special license. Non-profit use is freely available to researchers, hospitals, and AI companies worldwide. Commercial use requires a 10% allocation of revenue to cancer charities in the country of use. As enforcing this mandate is challenging, we welcome suggestions for commercial users (e.g., a one-time payment to charities every five years).
