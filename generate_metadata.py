import os
import glob 
import json
import uuid # Use uuid.uuid4() for privacy safe unique generator
import argparse
from collections import defaultdict
from subprocess import call
from natsort import natsorted


'''
    1. Generate metadata json file
    2. For each image generate template json object with all necessary fields
    3. Move and rename files to a final "Dataset" folder, e.g., similar to Arabic dataset
    
    Examples: 
        * Bulgarian
            python generate_metadata.py --source_name="2dzi_bzo_v1-otgovori_20052024" --grade="12" --language="Bulgarian" --subject="Biology" --subject_group="Natural Sciences" --date="2024"
        * Hungarian
            python generate_metadata.py --source_name="e_kozg_24okt_fl" --grade="12" --language="Hungarian" --subject="Math" --subject_group="Sciences" --date="2024"
'''

DEFAULT_DATASET_DIR = r'dataset'
EXTRACTED_IMAGES_DIR = r'00_Data\Prepared Data\extracted_images'

def create_metadata_object(uuid, old_img_path, new_path, info):
    new_obj = {}
    new_obj['id'] = uuid
    new_obj['img_path'] = new_path
    new_obj['original_img_name'] = old_img_path
    new_obj['source_file'] = info['source_name']
    new_obj['answer_key'] = '' # A or B or C or D
    new_obj['type'] = os.path.basename(old_img_path).removeprefix('cropped_image_').split('_')[0]
    new_obj['grade'] = info['grade']
    new_obj['subject'] = info['subject']
    new_obj['subject_grouped'] = info['subject_group']
    new_obj['language'] = info['language']
    new_obj['chemical_structure'] = 0
    new_obj['table'] = 0
    new_obj['figure'] = 0
    new_obj['graph'] = 0
    new_obj['date'] = info['date']
    return new_obj

def copy_and_rename_file(source, dest):
    '''
    Rename using random UUID (keep track of original pdf + page + cropped item number)
    '''
    os.system(fr'copy "{source}" "{dest}"')
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default=DEFAULT_DATASET_DIR,  type=str, help='path to new dataset directory')
    parser.add_argument('--img_dir', default=EXTRACTED_IMAGES_DIR, type=str, help='path to extracted images directory')
    parser.add_argument('--source_name', type=str, help='pdf source name for the images', required=True)
    parser.add_argument('--grade', type=str, help='exam grade', required=True)
    parser.add_argument('--language', type=str, help='exam language', required=True)
    parser.add_argument('--subject', type=str, help='exam subject', required=True)
    parser.add_argument('--date', type=str, help='exam date', required=True)
    parser.add_argument('--subject_group', type=str, help='exam subject')
    args = parser.parse_args()

    #Information on pdf level
    info = defaultdict(str)
    info['source_name']=args.source_name
    info['language']=args.language
    info['grade']=args.grade
    info['subject']=args.subject
    info['subject_group']=args.subject_group
    info['date']=args.date
    
    cropped_questions_paths = os.path.join(args.img_dir,args.source_name + '*/*')
    cropped_questions_files = natsorted([f for f in glob.iglob(cropped_questions_paths, recursive=True) if os.path.isfile(f)])
    
    dataset_path = os.path.join(args.data_dir, args.language.lower() , args.source_name)
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
        print(f'Created directory: "{dataset_path}" successfully. Metadata and new image files will be created there.')
     
    metadata = []
    for i, file_full_path in enumerate(cropped_questions_files):
        new_id = str(uuid.uuid4())
        img_new_path = os.path.join(dataset_path, f'{i}_{new_id}.png')
        copy_and_rename_file(os.path.join(os.getcwd(), file_full_path), os.path.join(os.getcwd(),img_new_path))
        metadata.append(create_metadata_object(new_id, file_full_path, img_new_path, info))
    
    with open(os.path.join(dataset_path + '_metadata.json'), 'w', encoding='UTF-8') as f:
        f.write(json.dumps(metadata, indent=4, separators=(',', ': '), ensure_ascii=False))
        
    
    
    
    