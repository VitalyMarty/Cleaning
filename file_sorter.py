import os
import shutil
import re

def normalize(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9.]', '_', name)
    return name

def get_extensions(filename):
    return filename.split('.')[-1]

def get_known_extensions():
    return {
        'jpeg': 'Images',
        'png': 'Images',
        'jpg': 'Images',
        'svg': 'Images',
        'avi': 'Video',
        'mp4': 'Video',
        'mov': 'Video',
        'mkv': 'Video',
        'doc': 'Docs',
        'docx': 'Docs',
        'txt': 'Docs',
        'pdf': 'Docs',
        'xlsx': 'Docs',
        'pptx': 'Docs',
        'mp3': 'Music',
        'ogg': 'Music',
        'wav': 'Music',
        'amr': 'Music',
        'zip': 'Archives',
        'gz': 'Archives',
        'tar': 'Archives'
    }

def sort_folder(folder_path, known_extensions):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                extension = get_extensions(file)
                if extension in known_extensions:
                    category = known_extensions[extension]
                else:
                    category = 'Unknown'

                dest_folder = os.path.join(folder_path, category)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)

                dest_path = os.path.join(dest_folder, normalize(file))
                shutil.move(file_path, dest_path)

def get_unknown_extensions(folder_path, known_extensions):
    unknown_extensions = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            extension = get_extensions(file)
            if extension not in known_extensions:
                unknown_extensions.add(extension)
    return unknown_extensions
