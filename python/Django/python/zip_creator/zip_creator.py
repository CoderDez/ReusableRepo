from io import BytesIO
from zipfile import ZipFile

class ZipCreator():
    """class for creating a zip file of pdfs.
    
    instance methods:
    - populate_zip_files(self, files:dict) -> BytesIO"""

    def populate_zip_files(self, files:dict, file_extension: str) -> BytesIO:
        content = BytesIO()
        with ZipFile(content, "w") as zipObj:
            for name, bytes in files.items():
                zipObj.writestr(name + file_extension, bytes)
        return content.getvalue()
            