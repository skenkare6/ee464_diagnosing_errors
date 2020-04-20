import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './database_managers')))
from SourceFile import SourceFile # pylint: disable=import-error

def getJson(filepath):
    file = SourceFile.get_by_file_path(filepath)
    return file.to_json_string()
