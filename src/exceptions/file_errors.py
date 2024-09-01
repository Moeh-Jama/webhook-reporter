"""All errors and Exceptions related to the file format"""



class MalformedFile(Exception):
    def __init__(self, file: str):
        self.message = f"The file '{file}' is contains errors. Cannot parse it."
        super().__init__(self.message)

class FileMissingAttributes(Exception):
    def __init__(self, file: str):
        self.message = f"The file '{file}' is missing crucial attributes."
        super().__init__(message=self.message)