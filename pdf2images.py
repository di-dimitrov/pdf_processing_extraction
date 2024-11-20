from pdf2image import convert_from_path
import os
from tqdm import tqdm
import argparse
import glob

PDF_DEFAULT_DIR=r'exam_pdfs/'
IMG_DESTINATION_DIR = r'00_Data/Prepared Data/images'

def get_pdf_files(root_dir):
    pdf_files = []
    #root_dir_globed = os.path.join(root_dir,'**','*')
    #files_list = [f for f in glob.iglob(img_dir_globed, recursive=True) if os.path.isfile(f)]
    #for file in files_list:
    #    if file.lower().endswith('.pdf'):
    #        pdf_files.append(file)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(dirpath, filename))
    return pdf_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf_dir', default=PDF_DEFAULT_DIR,  type=str, help='path to directory of pdfs')
    parser.add_argument('--dest_dir', default=IMG_DESTINATION_DIR, type=str, help='path to destination of images')
    args = parser.parse_args()

    root_directory = args.pdf_dir
    pdf_files = get_pdf_files(root_directory)

    print("no of pdf files found:", len(pdf_files))
    for pdf_file in tqdm(pdf_files):
        print(f'Processing {pdf_file}')
        parent_directory = os.path.dirname(pdf_file)
        output_folder = os.path.splitext(os.path.basename(pdf_file))[0]
        save_dir = f'{args.dest_dir}/{output_folder}'
        if os.path.exists(save_dir):
            print(f"Directory '{save_dir}' already exists.")
            folder_exists = True
            if len(os.listdir(save_dir)) > 0:
                print(f"Directory '{save_dir}' has already been processed (non-empty directory). If this is not the case, please remove any files inside and rerun.")
                continue
        else:
            os.mkdir(f'{save_dir}')
            print(f"Directory '{save_dir}' created successfully.")
        images = convert_from_path(pdf_file, dpi=900)
        
        for i in tqdm(range(len(images))):            
            images[i].save(fr'{save_dir}/{output_folder}_page_{i}.png', 'PNG')
            print(f"Added image of page '{i}' successfully.")
