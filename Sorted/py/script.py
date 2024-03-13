import os
import shutil
import zipfile
import sys
import pathlib
from pathlib import Path

def normalize(file_extension):
    translation_table = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia'
    }

    file_extension = file_extension.lower()
    result = ""
    for char in file_extension:
        if char.isalpha():
            if char in translation_table:
                result += translation_table[char]
            else:
                result += char
        else:
            result += '_'
    return result

def sort_and_categorize_files(folder_path):
    file_categories = {
        'images': ('jpeg', 'png', 'jpg', 'svg'),
        'videos': ('avi', 'mp4', 'mov', 'mkv'),
        'documents': ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'),
        'music': ('mp3', 'ogg', 'wav', 'amr'),
        'archives': ('zip', 'gz', 'tar'),
        'other': ()
    }

    for category in file_categories.keys():
        (folder_path / category).mkdir(exist_ok=True)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(filename)
            normalized_extension = normalize(file_extension[1:])
            destination_folder = None

            for category, extensions in file_categories.items():
                if normalized_extension in extensions:
                    destination_folder = category
                    break

            if destination_folder:
                destination_folder_path = os.path.join(folder_path, destination_folder)
                destination_path = os.path.join(destination_folder_path, filename)

                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)

                shutil.move(file_path, destination_path)

            elif normalized_extension in file_categories['archives']:
                destination_folder = 'archives'
                destination_folder_path = os.path.join(folder_path, destination_folder)
                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)

                extract_archives(file_path, destination_folder)

        elif os.path.isdir(file_path) and filename.lower() != 'archives':
            sort_and_categorize_files(file_path)
            if not os.listdir(file_path):
                os.rmdir(file_path)

def extract_archives(archive_path, normalized_extension):
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        try:
            extract_folder = os.path.join(os.path.dirname(archive_path), normalize(normalized_extension))
            zip_ref.extractall(extract_folder)
        except zipfile.BadZipFile:
            print(f"Failed to extract {archive_path}. Removing...")
            os.remove(archive_path)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py folder_path")
        sys.exit(1)

    folder_path = pathlib.Path(sys.argv[1])
    if not folder_path.is_dir():
        print("Invalid folder path. Please provide a valid folder path.")
        sys.exit(1)

    sort_and_categorize_files(folder_path)
    print("Sorting and categorization completed!")

if __name__ == '__main__':
    main()
