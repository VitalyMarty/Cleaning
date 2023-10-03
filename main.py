import sys
import scan
import shutil
from pathlib import Path
from normalize import normalize
from files_generator import file_generator

# Transfer to category
def move_file(file_path, category):
    target_folder = folder_path / category
    target_folder.mkdir(parents=True, exist_ok=True)
    new_name = normalize(file_path.name)
    new_path = target_folder / new_name
    file_path.rename(new_path)

# Unzip and transfer
def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", ''))

    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))  # Unzip
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

# Delete empty folders
def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

# Gettin folders objects
def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

# Sort files by ext
def sort_files(folder_path):
    scan.scan(folder_path)

    extensions_mapping = {
        'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
        'videos': ('AVI', 'MP4', 'MOV', 'MKV'),
        'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
        'archives': ('ZIP', 'GZ', 'TAR')
    }

    for category, extensions in extensions_mapping.items():
        for extension in extensions:
            files = getattr(scan, f"{extension.lower()}_files")
            for file_path in files:
                move_file(file_path, category)

# Main sort fucntion
def main(folder_path):
    sort_files(folder_path)

    for file in scan.archives:
        handle_archive(file, folder_path, "ARCHIVE")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <folder_path>")
        sys.exit(1)
    
    path = sys.argv[1]
    print(f"Start in {path}")

    folder_path = Path(path)
    file_generator(folder_path) 
    main(folder_path)
