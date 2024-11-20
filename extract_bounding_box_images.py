from PIL import Image
import os
import glob

# Replace the paths below with the path to the image and the YOLO format txt file.
IMAGE_FOLDER_PATH = r'00_Data\Prepared Data\images'
TEXT_FOLDER_PATH = r'00_Data\Prepared Data\bounding_boxes'
EXTRACTED_FOLDER_NAME = r'extracted_images'

def read_yolo_format_txt(txt_file, image_height, image_width):
    with open(txt_file, 'r') as file:
        lines = file.readlines()
    bounding_boxes = []
    question_types = []
    for line in lines:
        class_id, center_x, center_y, width, height = map(float, line.strip().split())
        left = int((center_x - width / 2) * image_width)
        upper = int((center_y - height / 2) * image_height)
        right = int((center_x + width / 2) * image_width)
        lower = int((center_y + height / 2) * image_height)
        bounding_boxes.append((left, upper, right, lower))
        question_types.append('text' if class_id == 0 else 'image')
    
    return question_types, bounding_boxes

def extract_images_from_bounding_boxes(image_path, txt_file, file_name, parent_directory):
    try:
        with Image.open(image_path) as img:
            image_width, image_height = img.size
            question_types, bounding_boxes = read_yolo_format_txt(txt_file, image_height, image_width)
            if not len(bounding_boxes):
                return
            if os.path.exists(f'{parent_directory}/{file_name}'):
                print(f"Directory '{file_name}' already exists.")
                folder_exists = True
            else:
                os.mkdir(f'{parent_directory}/{file_name}')
                print(f"Directory '{file_name}' created successfully.")
            for i, bbox in enumerate(bounding_boxes):
                cropped_image = img.crop(bbox)
                output_file = f"{parent_directory}/{file_name}/cropped_image_{question_types[i]}_{i}.jpg"
                cropped_image.save(output_file)
                print(f"Image {i + 1} extracted and saved as '{output_file}'.")
    except Exception as e:
        print(f"Failed to extract images from bounding boxes: {e}")

def get_sorted_files_in_folder(folder_path):
    #files_in_folder = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    img_dir_globed = os.path.join(folder_path,'**','*')
    files_in_folder = [f for f in glob.iglob(img_dir_globed, recursive=True) if os.path.isfile(f)]
    sorted_files = sorted(files_in_folder)
    return sorted_files


parent_directory = os.path.join(os.path.dirname(IMAGE_FOLDER_PATH), EXTRACTED_FOLDER_NAME)
sorted_image_paths = get_sorted_files_in_folder(IMAGE_FOLDER_PATH)
sorted_bbox_paths = get_sorted_files_in_folder(TEXT_FOLDER_PATH)

for image_path, txt_file in zip(sorted_image_paths, sorted_bbox_paths):
    file_name_with_extension = os.path.basename(image_path)
    file_name, extension = os.path.splitext(file_name_with_extension)
    extract_images_from_bounding_boxes(image_path, txt_file, file_name, parent_directory)
