import os
import re
import zipfile


def get_file_extension(filename):
    """
    从文件名中获取扩展名，支持复合扩展名
    """
    # 匹配复合扩展名（例如 .tar.gz）或常规扩展名
    match = re.search(r'\.([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?)$', filename)
    if match:
        return match.group(1)
    else:
        return None
    

def compress_file(file_path, zip_file_path):
    """
    压缩单个文件到 ZIP 文件中
    :param file_path: 要压缩的文件路径
    :param zip_file_path: 生成的 ZIP 文件路径
    """
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=os.path.basename(file_path))
        print(f"File '{file_path}' has been compressed to '{zip_file_path}'")


def compress_folder(folder_path, zip_file_path):
    """
    压缩整个文件夹到 ZIP 文件中
    :param folder_path: 要压缩的文件夹路径
    :param zip_file_path: 生成的 ZIP 文件路径
    """
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=arc_name)
        print(f"Folder '{folder_path}' has been compressed '{zip_file_path}'")