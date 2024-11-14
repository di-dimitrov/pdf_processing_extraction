from pdf2image import convert_from_path
import os
from tqdm import tqdm
import argparse

def get_pdf_files(root_dir):
    pdf_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(dirpath, filename))
    return pdf_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf_dir', type=str, help='path to directory of pdfs')
    args = parser.parse_args()

    root_directory = args.pdf_dir
    pdf_files = get_pdf_files(root_directory)

    print("no of pdf files found:", len(pdf_files))
    for pdf_file in tqdm(pdf_files):
        print(f'Processing {pdf_file}')
        parent_directory = os.path.dirname(pdf_file)
        output_folder = os.path.splitext(os.path.basename(pdf_file))[0]
        images = convert_from_path(pdf_file, dpi=900)
        if os.path.exists(f'{parent_directory}/{output_folder}'):
            print(f"Directory '{parent_directory}/{output_folder}' already exists.")
            folder_exists = True
        else:
            os.mkdir(f'{parent_directory}/{output_folder}')
            print(f"Directory '{parent_directory}/{output_folder}' created successfully.")
        for i in tqdm(range(len(images))):            
            images[i].save(f'{parent_directory}/{output_folder}/page_{i}.png', 'PNG')
            print(f"Added image of page '{i}' successfully.")
