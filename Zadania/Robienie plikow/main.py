import os
import random
import shutil
import tarfile
import zipfile

def read_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

def generate_random_filename(word):
    # Generate a random number
    number = str(random.randint(100, 999))
    # Generate a random special character
    special_chars = ['-', '_', '@', '#', '$', '%', '&']
    special_char = random.choice(special_chars) if random.random() < 0.5 else ''
    # Include a space at random
    space = ' ' if random.random() < 0.5 else ''
    return word + space + number + special_char + '.txt'

def create_files(words, directory, extensions, backup_directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
    filenames = []
    for word in words:
        filename = generate_random_filename(word)
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as f:
            pass
        filenames.append(filename)
        print(f'Created file: {os.path.join(directory, filename)}')
    # Change file extensions
    for filename, extension in zip(filenames, extensions):
        new_filename = filename[:-4] + '.' + extension.lower()
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
        # Copy files to backup directory
        shutil.copy2(os.path.join(directory, new_filename), backup_directory)

def create_archive(directory, archive_type):
    archive_name = os.path.join(directory, directory + '.' + archive_type)
    if archive_type == 'zip':
        with zipfile.ZipFile(archive_name, 'w') as archive:
            for foldername, subfolders, filenames in os.walk(directory):
                for filename in filenames:
                    archive.write(os.path.join(foldername, filename), os.path.relpath(os.path.join(foldername,filename), directory))
    elif archive_type in ['gz', 'tar']:
        with tarfile.open(archive_name, 'w:gz' if archive_type == 'gz' else 'w') as archive:
            archive.add(directory, arcname=os.path.basename(directory))
    print(f'Created archive: {archive_name}')

def move_files_to_directory(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    for foldername, subfolders, filenames in os.walk(source_directory):
        for filename in filenames:
            new_target_directory = target_directory + foldername[len(source_directory):]
            if not os.path.exists(new_target_directory):
                os.makedirs(new_target_directory)
            shutil.move(os.path.join(foldername, filename), os.path.join(new_target_directory, filename))

def remove_directory(directory):
    shutil.rmtree(directory)

# Read words from both files
english_words = read_words('words.txt')
polish_words = read_words('polish_words.txt')

# Define file types
file_types = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
}

# Flatten the file types into a list and shuffle it
extensions = [ext for sublist in file_types.values() for ext in sublist]
random.shuffle(extensions)

# Create 18 files for each set of words and change their extensions
create_files(english_words[:18], 'EnglishFiles', extensions[:18], 'EnglishFiles/backup')
create_files(polish_words[:18], 'PolishFiles', extensions[:18], 'PolishFiles/kopia')

# Create archives
create_archive('EnglishFiles', 'zip')
create_archive('EnglishFiles', 'gz')
create_archive('EnglishFiles', 'tar')
create_archive('PolishFiles', 'zip')
create_archive('PolishFiles', 'gz')
create_archive('PolishFiles', 'tar')

# Move all files to the 'Bałagan' directory
move_files_to_directory('EnglishFiles', 'Bałagan')
move_files_to_directory('PolishFiles', 'Bałagan')

# Remove the 'EnglishFiles' and 'PolishFiles' directories
remove_directory('EnglishFiles')
remove_directory('PolishFiles')