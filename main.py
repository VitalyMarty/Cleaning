import sys
from pathlib import Path
from file_sorter import sort_folder, get_known_extensions, get_unknown_extensions

def main(folder_path):
    folder_path = Path(folder_path)
    print("Start in", folder_path)

    if not folder_path.exists():
        print("Folder does not exist.")
        return

    known_extensions = get_known_extensions()
    unknown_extensions = get_unknown_extensions(folder_path, known_extensions)

    print("Sorting files...")
    sort_folder(folder_path, known_extensions)

    print("Files in each category:")
    for ext, category in known_extensions.items():
        category_folder = folder_path / category
        if category_folder.exists():
            print(f"{category}:")
            for file_path in category_folder.iterdir():
                print(file_path)

    print("Known extensions:", known_extensions)
    print("Unknown extensions:", unknown_extensions)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <folder_path>")
    else:
        main(sys.argv[1])
