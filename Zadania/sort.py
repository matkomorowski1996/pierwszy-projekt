import os
import shutil
import zipfile
import tarfile
import unicodedata

def normalize(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return ''.join(c if c.isalnum() or c in {'_', '.'} else '_' for c in text)

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            process_folder(dir_path)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            extension = file.split('.')[-1].upper()

            if extension in {'JPEG', 'PNG', 'JPG', 'SVG'}:
                move_file(file_path, 'images')
            elif extension in {'AVI', 'MP4', 'MOV', 'MKV'}:
                move_file(file_path, 'video')
            elif extension in {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'}:
                move_file(file_path, 'documents')
            elif extension in {'MP3', 'OGG', 'WAV', 'AMR'}:
                move_file(file_path, 'audio')
            elif extension in {'ZIP', 'GZ', 'TAR'}:
                extract_archive(file_path, 'archives')
            else:
                print(f"Unknown extension: {extension} for file: {file_path}")

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path) and dir_name not in {'archives', 'video', 'audio', 'documents', 'images'}:
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")

def move_file(file_path, category):
    destination_folder = os.path.join(folder_path, category)
    os.makedirs(destination_folder, exist_ok=True)

    normalized_name = normalize(os.path.basename(file_path))
    new_file_path = os.path.join(destination_folder, normalized_name)

    shutil.move(file_path, new_file_path)
    print(f"Moved {file_path} to {new_file_path}")

def extract_archive(file_path, category):
    destination_folder = os.path.join(folder_path, category)
    os.makedirs(destination_folder, exist_ok=True)

    normalized_name = normalize(os.path.splitext(os.path.basename(file_path))[0])
    extract_folder = os.path.join(destination_folder, normalized_name)

    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
    elif file_path.endswith('.tar') or file_path.endswith('.gz'):
        with tarfile.open(file_path, 'r') as tar_ref:
            tar_ref.extractall(extract_folder)

    print(f"Extracted {file_path} to {extract_folder}")

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)

    global folder_path
    folder_path = sys.argv[1]
    process_folder(folder_path)

if __name__ == "__main__":
    main()
