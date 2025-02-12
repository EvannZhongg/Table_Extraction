# PDF Extraction

This project focuses on extracting parameters from PDF files, specifically by recognizing miages and tables. The main tasks include:

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
## Usage

Once the models are set up,Once the model is built, you can start extracting tables and text from images.

This project makes use of  [wyf3](https://github.com/wyf3/llm_related/tree/main)
