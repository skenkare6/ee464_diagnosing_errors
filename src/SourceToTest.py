import json

from SourceFile import SourceFile

def getJson(filepath):
    file = SourceFile.get_by_file_path(filepath)
    return file.to_json_string()
