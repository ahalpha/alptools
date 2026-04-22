import mmap
import array
import struct
from typing import Literal


class MMapReader:
    def __init__(self, mm: mmap.mmap, endian: Literal["little", "big"] = "little"):
        self.mm = mm
        self.offset = 0
        self._is_be = endian == "big"

    @property
    def i8(self):
        data = struct.unpack("b", self.mm[self.offset : self.offset + 1])[0]
        self.offset += 1
        return data

    @property
    def u8(self):
        data = struct.unpack("B", self.mm[self.offset : self.offset + 1])[0]
        self.offset += 1
        return data

    @property
    def i16(self):
        data = struct.unpack(">h" if self._is_be else "<h", self.mm[self.offset : self.offset + 2])[0]
        self.offset += 2
        return data

    @property
    def u16(self):
        data = struct.unpack(">H" if self._is_be else "<H", self.mm[self.offset : self.offset + 2])[0]
        self.offset += 2
        return data

    @property
    def i32(self):
        data = struct.unpack(">i" if self._is_be else "<i", self.mm[self.offset : self.offset + 4])[0]
        self.offset += 4
        return data

    @property
    def u32(self):
        data = struct.unpack(">I" if self._is_be else "<I", self.mm[self.offset : self.offset + 4])[0]
        self.offset += 4
        return data

    @property
    def i64(self):
        data = struct.unpack(">q" if self._is_be else "<q", self.mm[self.offset : self.offset + 8])[0]
        self.offset += 8
        return data

    @property
    def u64(self):
        data = struct.unpack(">Q" if self._is_be else "<Q", self.mm[self.offset : self.offset + 8])[0]
        self.offset += 8
        return data

    @property
    def f32(self):
        data = struct.unpack(">f" if self._is_be else "<f", self.mm[self.offset : self.offset + 4])[0]
        self.offset += 4
        return data

    @property
    def f64(self):
        data = struct.unpack(">d" if self._is_be else "<d", self.mm[self.offset : self.offset + 8])[0]
        self.offset += 8
        return data

    @property
    def bool(self):
        data = self.mm[self.offset] != 0
        self.offset += 1
        return data

    def bytes(self, size: int):
        data = self.mm[self.offset : self.offset + size]
        self.offset += size
        return data

    def str(self, size: int, encoding: str = "utf-16", errors: str = "strict"):
        data = self.mm[self.offset : self.offset + size].decode(encoding, errors)
        self.offset += size
        return data

    def list(self, type: str, count: int):
        array_obj = array.array(type)
        size = array_obj.itemsize * count
        data = array_obj.frombytes(self.mm[self.offset : self.offset + size])
        self.offset += size
        return data

    def none(self, size: int = 1):
        self.offset += size
        return None
