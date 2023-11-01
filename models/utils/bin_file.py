from .common_functions import file_read


class BinFile:
    def open_file(self, file_location:str):
        self.file_location = file_location
        self.file_content = file_read(self.file_location)
        self.size = len(self.file_content)
        self.magic_number = self.file_content[:4]

    def save_file(self,file_location=None):
        file_location = self.file_location = file_location or self.file_location
        with open(self.file_location,'wb') as bf:
            bf.write(self.file_content)
