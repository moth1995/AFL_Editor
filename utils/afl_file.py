from .bin_file import BinFile
from .common_functions import to_b_int32, to_int

class AFLFile(BinFile):
    AFL_MAGIC_NUMBER = bytearray([0x41,0x46,0x4C,0x00])
    EXTRA_HEADER_DATA = bytearray([0x01,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF])
    MAX_LEN = 32
    HEADER_SIZE = 16

    def from_afl(self, file_location:str):
        self.open_file(file_location)
        if self.magic_number != self.AFL_MAGIC_NUMBER:
            raise ValueError("This is not an AFL File!")
        self.nums_of_files = to_int(self.file_content[12:16])
        self.read_files_from_bytes()

    def from_afs(self, nums_of_files: int, file_location:str):
        self.nums_of_files = nums_of_files
        self.file_location = file_location
        data = b''
        for i in range(self.nums_of_files):
            base_bytes = bytearray([0] * self.MAX_LEN)
            new_name = f"unnamed_{i}.bin".encode("utf-8")
            base_bytes[:len(new_name)] = new_name
            data+=base_bytes
        header = self.AFL_MAGIC_NUMBER + self.EXTRA_HEADER_DATA + to_b_int32(self.nums_of_files)
        self.file_content = header + data
        self.size = len(self.file_content)
        self.read_files_from_bytes()

    def read_files_from_bytes(self):
        self.files = [
            self.file_content[i : i + self.MAX_LEN].partition(b"\0")[0].decode('utf-8') 
            for i in range(
                self.HEADER_SIZE, self.size, self.MAX_LEN
            )
        ]

    def set_name(self, file_idx, new_name:str):
        if 0 < len(new_name) < self.MAX_LEN:
            file_name_bytes = [0] * self.MAX_LEN
            new_name_bytes = str.encode(new_name, "utf-8","ignore")
            file_name_bytes[: len(new_name_bytes)] = new_name_bytes
            for i, byte in enumerate(file_name_bytes):
                self.file_content[self.HEADER_SIZE + (file_idx * self.MAX_LEN) + i] = byte
            self.read_files_from_bytes()
        else:
            raise ValueError("File name can't be empty or bigger than 60 characters")

    def add_file(self, quantity_of_files):
        data = b''
        for i in range(quantity_of_files):
            base_bytes = bytearray([0] * self.MAX_LEN)
            new_name = f"unnamed_{self.nums_of_files+i}.bin".encode("utf-8")
            base_bytes[:len(new_name)] = new_name
            data+=base_bytes
            self.nums_of_files+=1
        self.file_content+=data
        self.file_content[12:16] = to_b_int32(self.nums_of_files)
        self.size=len(self.file_content)
        self.read_files_from_bytes()
