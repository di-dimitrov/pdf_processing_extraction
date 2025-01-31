# Installation


## Create Virtual Environment (Anaconda recommended)

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

Additionally, install poppler in your work env using a package manager `pip install python-poppler`

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

Straightforward usecase: Put exam pdfs in `./exam_pdfs` folder. Run the script `python pdf2images.py`. It takes a while but the script will create a separate folder for each pdf with images (1 per page in the pdf).

Already processed PDFs will be skipped when running the script (Checks if directory is empty). If you want to process a pdf again just delete the previously created directory.

## annotate_bboxes.py -> Annotating bounding boxes with proper classes (text or image)

After processing the pdfs into images, run the script `python annotate_bboxes.py`. Default image directory is `'00_Data/Prepared Data/images'` and default bbox directory is `'00_Data/Prepared Data/bounding_boxes'`. 

(Not recommended) To run with custom dir use this command: `python annotate_bboxes.py --images_path='custom/path/directory/images' --bbox_path='custom/path/directory/bbox'`

## extract_bounding_box_images.py -> Crop images from each page

After annotation is complete, we have to extract the questions from the images by running  `python extract_bounding_box_images.py`.
The script creates a new directory (default value = `00_Data\Prepared Data\extracted_images`) and creates a subdirectory for each page for every processed pdf file.

 This script does not have arguments as it is very simple. The default paths are: 
```
IMAGE_FOLDER_PATH = r'00_Data\Prepared Data\images'
TEXT_FOLDER_PATH = r'00_Data\Prepared Data\bounding_boxes'
```

To modify them directly go inside the script and change to prefered path. If necessary add arg parser to enable argument passing as in previous steps.

## generate_metadata.py -> Initialize metadata.json file (to fill answers) and move images with randomized names

After extracting the cropped images, run with the following arguments:

```
python generate_metadata.py --source_name="<pdf-name>" --grade="<questions_difficulty> --language="<question_language> --subject="<exam_subject>" --subject_group="exam_subject_group" --date="<exam_date>"
```

Example for Bulgarian:

```
python generate_metadata.py --source_name="2dzi_bzo_v1-otgovori_20052024" --grade="12" --language="Bulgarian" --subject="Biology" --subject_group="Natural Sciences" --date="2024"
```

Results of the script are located in the `dataset/` folder of the repository. A subdirectory is created for each language. 

## image_loader.py -> load images, select correct answers, and select visual elements `graph/table/chemical_structure/figure`
Note: Interface is very simple, i.e., it can be improved.

To start the application run:
```
uvicorn image_loader:app --reload
```
An empty input field will appear that expects input <file_path> for `*_metadata.json` file. Example: `dataset/bulgarian/Matura_2024_Math_metadata.json`

This will open the json and load the first question with empty `answer_key`. Select the answer (based on image/document with answers) and then select the approriate visual elements (if such apply). Press `Submit` to continue to next element. Once the json is processed you have to input another <file_path>. 

_Note: Submitting modifies the existing json.

## Manual answer annotation (if image_loader cannot be used)

After executing the above steps, open the generated `<source_name>_metadata.json` file. Using the original PDF or a separate PDF for answers, depending on the exam format, fill the `answer_key` field with the correct answer: `A or B or C or D` and if the question contains any visual information change the value of 
`chemical_structure`, `table`, `figure`, `graph` accordingly (by default value is 0, change it to 1 if the question contains the respective visual element) 