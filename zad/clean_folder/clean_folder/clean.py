import os
import shutil
import zipfile
import unicodedata

def normalize(text):
    normalized_text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    normalized_text = ''.join(c if c.isalnum() or c in ['.', '_'] else '_' for c in normalized_text)
    return normalized_text

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            extension = os.path.splitext(file_name)[1].upper()[1:]

            if extension in ['JPEG', 'PNG', 'JPG', 'SVG']:
                destination_folder = 'images'
            elif extension in ['AVI', 'MP4', 'MOV', 'MKV']:
                destination_folder = 'video'
            elif extension in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
                destination_folder = 'documents'
            elif extension in ['MP3', 'OGG', 'WAV', 'AMR']:
                destination_folder = 'audio'
            elif extension in ['ZIP', 'GZ', 'TAR']:
                destination_folder = 'archives'
                # Unzip archive
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(root, normalize(file_name[:-4])))
                # Remove original archive
                os.remove(file_path)
                continue  # Skip to the next iteration to avoid further processing for the archive file
            else:
                destination_folder = 'unknown'

            destination_folder_path = os.path.join(root, destination_folder)
            if not os.path.exists(destination_folder_path):
                os.makedirs(destination_folder_path)

            new_file_name = normalize(file_name)
            new_file_path = os.path.join(destination_folder_path, new_file_name)
            shutil.move(file_path, new_file_path)

    # Remove empty folders
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            if not os.listdir(directory_path):
                os.rmdir(directory_path)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_folder(folder_path)
