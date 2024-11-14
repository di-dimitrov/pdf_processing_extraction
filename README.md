# Installation


## Create Virtual Environment

To create a new Anaconda environment, run the following command:

```
conda create -n exams python=3.10
```
Anaconda is good because you can easily use different python installations for environments

To create virtual environment with venv, run the following command:

```
python3 -m venv exams
```

Next, activate the virtual environment:

With Anaconda
```
conda activate exams
```

With python venv, first checkout the venv source folder and then run
```
source activate 
```

## Install dependencies

```bash
pip install -r requirements.txt
```


## Unzip poppler (pdf editor) - poppler-24.08.0-0.zip (linux users can follow official tool page for installation)

After unzip in desired location, add bin/ to PATH env variables. This will make it available for pdf2image script.

## Common issues: ModuleNotFoundError: No module named 'cv2'

This can happen due to some issues with OpenCV library. If you are using conda run the following command: 
```
conda install opencv
```

If using Pip
```
pip3 install opencv-python
```

# Usage

## pdf2images.py -> Convert exam pdfs to list of images (1 image per page)

Straightforward usecase: Put exam pdfs in `./exam_pdfs` folder. Run the script `python pdf2images.py --pdf_dir="exam_pdfs/"`. It takes a while but the script will create a separate folder for each pdf with images (1 per page in the pdf).

## annotate_bboxes.py -> Annotating bounding boxes with proper classes (we can add classes for answers)

You can move the images from the previous step to `'00_Data/Prepared Data/images'` and then the command is to run the script is simple `python annotate_bboxes.py`. Default image directory is `'00_Data/Prepared Data/images'` and default bbox directory is `'00_Data/Prepared Data/bounding_boxes'`. 

To run with custom dir use this command: `python annotate_bboxes.py --images_path='custom/path/directory/images' --bbox_path='custom/path/directory/bbox'`

## extract_bounding_box_images.py

After annotation is complete, we have to extract the questions from the images by running  `python extract_bounding_box_images.py`. This script does not have arguments as  it is very simple. The default paths are: 
```
IMAGE_FOLDER_PATH = r'00_Data\Prepared Data\images'
TEXT_FOLDER_PATH = r'00_Data\Prepared Data\bounding_boxes'
```

To modify them directly go inside the script and change to prefered path. If necessary add arg parser to enable argument passing as in previous steps.