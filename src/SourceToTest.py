import json
from SourceFile import SourceFile # pylint: disable=import-error

def getJson(filepath):
    file = SourceFile.get_by_file_path(filepath)
    return file.to_json_string()
