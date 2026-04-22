import io
import array
import struct
import pathlib
from typing import IO, Literal, Union

from .__debug_detector import DebugDetector


class IOReader:
    def __init__(self, file: IO[bytes] | bytes | bytearray | str, endian: Literal["little", "big"] = "little"):
        if isinstance(file, str) or isinstance(file, pathlib.Path):
            self.file = open(file, "rb")
            self._is_temp_mode = True
        elif isinstance(file, bytes) or isinstance(file, bytearray):
            self.file = io.BytesIO(file)
            self._is_temp_mode = True
        else:
            self.file = file
            self._is_temp_mode = False
        self._size = None
        self._is_be = endian == "big"

    def read(self, size: int) -> bytes:
        buf = self.file.read(size)
        if DebugDetector.is_hover_eval():
            self.offset -= size
        return buf

    @property
    def endian(self) -> Literal["little", "big"]:
        return "big" if self._is_be else "little"

    @endian.setter
    def endian(self, endian: Literal["little", "big"]):
        self._is_be = endian == "big"
        return

    @property
    def i8(self) -> int:
        return struct.unpack("b", self.read(1))[0]

    @property
    def u8(self) -> int:
        return struct.unpack("B", self.read(1))[0]

    @property
    def i16(self) -> int:
        return struct.unpack(">h" if self._is_be else "<h", self.read(2))[0]

    @property
    def u16(self) -> int:
        return struct.unpack(">H" if self._is_be else "<H", self.read(2))[0]

    @property
    def i32(self) -> int:
        return struct.unpack(">i" if self._is_be else "<i", self.read(4))[0]

    @property
    def u32(self) -> int:
        return struct.unpack(">I" if self._is_be else "<I", self.read(4))[0]

    @property
    def i64(self) -> int:
        return struct.unpack(">q" if self._is_be else "<q", self.read(8))[0]

    @property
    def u64(self) -> int:
        return struct.unpack(">Q" if self._is_be else "<Q", self.read(8))[0]

    @property
    def i128(self) -> int:
        if self._is_be:
            high, low = struct.unpack(">qq", self.file.read(16))
        else:
            low, high = struct.unpack("<qq", self.file.read(16))
        return (high << 64) | (low & 0xFFFFFFFFFFFFFFFF)

    @property
    def u128(self) -> int:
        if self._is_be:
            high, low = struct.unpack(">QQ", self.file.read(16))
        else:
            low, high = struct.unpack("<QQ", self.file.read(16))
        return (high << 64) | (low & 0xFFFFFFFFFFFFFFFF)

    @property
    def f32(self) -> float:
        return struct.unpack(">f" if self._is_be else "<f", self.read(4))[0]

    @property
    def f64(self) -> float:
        return struct.unpack(">d" if self._is_be else "<d", self.read(8))[0]

    @property
    def bool(self) -> bool:
        return self.read(1)[0] != 0

    @property
    def byte(self) -> bytes:
        return self.read(1)

    def bytes(self, size: int) -> bytes:
        return self.read(size)

    def str(self, size: int, encoding: str = "utf-8", errors: str = "strict") -> str:
        return self.read(size).decode(encoding, errors)

    def list(self, type: str, size: int) -> list:
        return array.array(type).fromfile(self.file, size)

    def none(self, size: int = 1) -> None:
        self.file.seek(size, 1)
        return None

    @property
    def offset(self) -> int:
        return self.file.tell()

    @offset.setter
    def offset(self, offset) -> None:
        self.file.seek(offset)
        return

    @property
    def size(self) -> int:
        if self._size != None:
            return self._size
        offset = self.file.tell()
        self.file.seek(0, 2)
        self._size = self.file.tell()
        self.file.seek(offset)
        return self._size

    def read_to_none(self):
        result = bytearray()
        while self.offset != self.size and (byte := self.u8) != 0:
            result.append(byte)
        return result

    def to_search(self, pattern: Union[bytes, str], whence=1):
        if isinstance(pattern, str):
            pattern = pattern.encode("utf-8")
        pattern_1 = pattern[:1]
        pattern_2 = pattern[1:]
        pattern_2_size = len(pattern_2)
        cached_offset = self.offset
        if whence == 0:
            self.offset = 0
        if whence == 2:
            self.offset = self.size - len(pattern)
        while (byte := self.byte) != b"":
            if whence == 2 and self.offset == -1:
                break
            if byte == pattern_1:
                if self.bytes(pattern_2_size) == pattern_2:
                    self.offset -= len(pattern)
                    return True
                else:
                    self.offset -= pattern_2_size
            if whence == 2:
                self.offset -= 2
        self.offset = cached_offset
        return False

    def align(self, padding=4, offset=0):
        curr_offset = self.file.tell()
        if (mod := (curr_offset + offset) % padding) != 0:
            self.file.seek(curr_offset + padding - mod)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._is_temp_mode:
            self.file.close()

    def close(self):
        self.file.close()
