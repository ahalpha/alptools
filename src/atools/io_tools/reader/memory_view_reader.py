import array
from typing import Literal


class MemoryViewReader:
    def __init__(self, mv: memoryview, endian: Literal["little", "big"] = "little"):
        self.mv = mv
        self.offset = 0
        self._is_be = endian == "big"

    @property
    def i8(self):
        data = self.mv[self.offset : self.offset + 1].cast("b")[0]
        self.offset += 1
        return data

    @property
    def u8(self):
        data = self.mv[self.offset : self.offset + 1].cast("B")[0]
        self.offset += 1
        return data

    @property
    def i16(self):
        data = self.mv[self.offset : self.offset + 2].cast("h")[0]
        self.offset += 2
        return data

    @property
    def u16(self):
        data = self.mv[self.offset : self.offset + 2].cast("H")[0]
        self.offset += 2
        return data

    @property
    def i32(self):
        data = self.mv[self.offset : self.offset + 4].cast("i")[0]
        self.offset += 4
        return data

    @property
    def u32(self):
        data = self.mv[self.offset : self.offset + 4].cast("I")[0]
        self.offset += 4
        return data

    @property
    def i64(self):
        data = self.mv[self.offset : self.offset + 8].cast("q")[0]
        self.offset += 8
        return data

    @property
    def u64(self):
        data = self.mv[self.offset : self.offset + 8].cast("Q")[0]
        self.offset += 8
        return data

    @property
    def f32(self):
        data = self.mv[self.offset : self.offset + 4].cast("f")[0]
        self.offset += 4
        return data

    @property
    def f64(self):
        data = self.mv[self.offset : self.offset + 8].cast("d")[0]
        self.offset += 8
        return data

    @property
    def bool(self):
        data = self.mv[self.offset] != 0
        self.offset += 1
        return data

    def bytes(self, size: int):
        data = self.mv[self.offset : self.offset + size]
        self.offset += size
        return data

    def str(self, size: int, encoding: str = "utf-16", errors: str = "strict"):
        data = self.mv[self.offset : self.offset + size].decode(encoding, errors)
        self.offset += size
        return data

    def list(self, type: str, count: int):
        size = array.array(type).itemsize * count
        data = self.mv[self.offset : self.offset + size].cast(type)
        self.offset += size
        return data

    def none(self, size: int = 1):
        self.offset += size
        return None
