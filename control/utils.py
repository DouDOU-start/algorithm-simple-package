import re


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