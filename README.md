# PDF Extraction

This project focuses on extracting parameters from PDF files, specifically by recognizing tables. The main tasks include:

## Table Extraction

The table extraction process utilizes the Cycle-CenterNet model for table structure recognition. The model is designed to identify structured tables in images and convert them into a format that a large language model can understand.

### Model Setup

1. **Clone the Model**: 
   First, install Git LFS and clone the table structure recognition model repository:

   ```bash
   git lfs install
   git clone https://www.modelscope.cn/iic/cv_dla34_table-structure-recognition_cycle-centernet.git
   ```

2. **Model Path**:
   After cloning the repository, set the absolute path to the model as follows:

   ```python
   model_path = "your_absolute_path_to_cv_dla34_table-structure-recognition_cycle-centernet"
   ```

## OCR Setup

To extract text from images, we use PaddleOCR. PaddleOCR is capable of recognizing text in different languages and works in conjunction with the table structure model.

### OCR Setup

Set the absolute paths for the OCR models:

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_gpu=True,
    lang='ch',  # Set language to Chinese ('ch')
    det_model_dir='your_absolute_path_to_ch_PP-OCRv4_det_infer',
    rec_model_dir='your_absolute_path_to_ch_PP-OCRv4_rec_infer',
    cls_model_dir='your_absolute_path_to_ch_ppocr_mobile_v2.0_cls_infer'
)
```

After starting the code, the PaddleOCR model will be automatically downloaded:

```bash
python main.py
```
or
```bash
python Table_Extraction.py
```
## Effect display
![image](https://github.com/user-attachments/assets/8e0f21d8-af6c-4da2-beb7-dcc7f5f73115)
![image](https://github.com/user-attachments/assets/45ad3906-09df-431e-a4ec-4f0779137195)

```
PartNumber | TotalCapacitance(Ct) @ 50 V,(pF) | TotalCapacitance(Ct) @ 0 V,(pF) | SeriesResistance (Rs),@10 mA,(②) | MinorityCarrierLifetime (TL)@ 10 mA(ns) | VoltageRating2(M) | I-RegionThickness(μm) | ThermalResistance(0JC)(°C/W)
Maximum | Typical | Maximum | Typical | Minimum | Nominal | Maximum

Switching Applications(continued)
 | APD0810-203 | 0.35 | 0.40 | 1.5 | 160 | 100 | 8 | 174
 | APD0810-210 | 0.40 | 0.45 | 1.5 | 160 | 100 | 8 | 75
 | APD0810-219 | 0.35 | 0.40 | 1.5 | 160 | 100 | 8 | 143
 | APD0810-240 | 0.35 | 0.40 | 1.5 | 160 | 100 | 8 | 155
 | APD1505-203 | 0.40 | 0.45@10V | 2.5 | 350 | 200 | 15 | 172
 | APD1505-210 | 0.40 | 0.45@10 V | 2.5 | 350 | 200 | 15 | 74
 | APD1505-219 | 0.40 | 0.45@10V | 2.5 | 350 | 200 | 15 | 142
 | APD1505-240 | 0.40 | 0.45 @ 10 V | 2.5 | 350 | 200 | 15 | 150
 | APD1510-203 | 0.35 | 0.40 | 2.0 | 300 | 200 | 15 | 168
 | APD1510-210 | 0.35 | 0.40 | 2.0 | 300 | 200 | 15 | 70
 | APD1510-219 | 0.35 | 0.40 | 2.0 | 300 | 200 | 15 | 137
 | APD1510-240 | 0.35 | 0.40 | 2.0 | 300 | 200 | 15 | 149
 | APD1520-203 | 0.40 | 0.45 | 1.2 | 900 | 200 | 15 | 155
 | APD1520-210 | 0.40 | 0.45 | 1.2 | 900 | 200 | 15 | 57
 | APD1520-219 | 0.45 | 0.50 | 1.2 | 900 | 200 | 15 | 124
 | APD1520-240 | 0.40 | 0.45 | 1.2 | 900 | 200 | 15 | 136

AttenuatorApplications
 | APD2220-203 | 0.45 | 0.50 | 4.0 | 100 | 100 | 50 | 132
 | APD2220-210 | 0.45 | 0.50 | 4.0 | 100 | 100 | 50 | 32
 | APD2220-219 | 0.40 | 0.45 | 4.0 | 100 | 100 | 50 | 104
 | APD2220-240 | 0.40 | 0.45 | 4.0 | 100 | 100 | 50 | 115
```

## Usage

Once the models are set up, you can start extracting tables and text from images.

This project makes use of  [wyf3](https://github.com/wyf3/llm_related/tree/main)
