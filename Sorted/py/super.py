import os
import sys
from pathlib import Path
from shutil import move
from zipfile import ZipFile, BadZipFile

def normalize(file_extension):
    image_extensions = ('.JPEG', '.PNG', '.JPG', '.SVG')
    video_extensions = ('.AVI', '.MP4', '.MOV', '.MKV')
    document_extensions = ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX')
    music_extensions = ('.MP3', '.OGG', '.WAV', '.AMR')
    archive_extensions = ('.ZIP', '.GZ', '.TAR')

    if file_extension.upper() in image_extensions:
        return 'images'
    elif file_extension.upper() in video_extensions:
        return 'videos'
    elif file_extension.upper() in document_extensions:
        return 'documents'
    elif file_extension.upper() in music_extensions:
        return 'music'
    elif file_extension.upper() in archive_extensions:
        return 'archives'
    else:
        return 'unknown'

def sort_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = folder_path / filename

        if file_path.is_file():
            _, file_extension = os.path.splitext(filename)
            destination_folder = normalize(file_extension).lower()

            if not (folder_path / destination_folder).exists():
                (folder_path / destination_folder).mkdir(parents=True)

            destination_path = folder_path / destination_folder / filename
            move(file_path, destination_path)

        elif file_path.is_dir():
            if filename.lower() not in ['archives', 'video', 'audio', 'documents', 'images', 'others']:
                sort_files(file_path)
                if not os.listdir(file_path):
                    file_path.rmdir()

            elif filename.lower() == 'archives':
                extract_archives(file_path)

def extract_archives(archive_folder):
    for archive_filename in os.listdir(archive_folder):
        archive_path = archive_folder / archive_filename
        if archive_path.is_file():
            _, archive_extension = os.path.splitext(archive_filename)
            if archive_extension.upper() in ('.ZIP', '.GZ', '.TAR'):
                extract_folder = archive_folder / normalize(archive_extension).lower()
                with ZipFile(archive_path, 'r') as zip_ref:
                    try:
                        zip_ref.extractall(extract_folder)
                    except BadZipFile:
                        print(f"Failed to extract {archive_filename} in {archive_folder}. Removing...")
                        archive_path.unlink()

def main():
    folder_path = Path(sys.argv[1])
    sort_files(folder_path)
    print("Files sorted successfully.")

if __name__ == "__main__":
    main()
