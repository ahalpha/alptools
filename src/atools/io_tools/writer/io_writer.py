import io
import sys
import array
import struct
import pathlib
from typing import IO, Literal, Iterable


class IOWriter:
    def __init__(
        self,
        file: IO[bytes] | str | pathlib.Path | None = None,
        endian: Literal["little", "big"] = "little",
    ):
        if file is None:
            self.file = io.BytesIO()
            self._is_temp_mode = True
            self._is_memory_mode = True
        elif isinstance(file, str) or isinstance(file, pathlib.Path):
            self.file = open(file, "wb")
            self._is_temp_mode = True
            self._is_memory_mode = False
        else:
            self.file = file
            self._is_temp_mode = False
            self._is_memory_mode = False

        self._size = None
        self._is_be = endian == "big"

    def write(self, data: bytes | bytearray | memoryview) -> None:
        self.file.write(data)
        self._size = None

    @property
    def endian(self) -> Literal["little", "big"]:
        return "big" if self._is_be else "little"

    @endian.setter
    def endian(self, endian: Literal["little", "big"]):
        self._is_be = endian == "big"

    def i8(self, value: int) -> None:
        self.write(struct.pack("b", value))

    def u8(self, value: int) -> None:
        self.write(struct.pack("B", value))

    def i16(self, value: int) -> None:
        self.write(struct.pack(">h" if self._is_be else "<h", value))

    def u16(self, value: int) -> None:
        self.write(struct.pack(">H" if self._is_be else "<H", value))

    def i32(self, value: int) -> None:
        self.write(struct.pack(">i" if self._is_be else "<i", value))

    def u32(self, value: int) -> None:
        self.write(struct.pack(">I" if self._is_be else "<I", value))

    def i64(self, value: int) -> None:
        self.write(struct.pack(">q" if self._is_be else "<q", value))

    def u64(self, value: int) -> None:
        self.write(struct.pack(">Q" if self._is_be else "<Q", value))

    def i128(self, value: int) -> None:
        if not -(1 << 127) <= value < (1 << 127):
            raise OverflowError("i128 value out of range")

        low = value & 0xFFFFFFFFFFFFFFFF
        high = value >> 64

        if self._is_be:
            self.write(struct.pack(">qQ", high, low))
        else:
            self.write(struct.pack("<Qq", low, high))

    def u128(self, value: int) -> None:
        if not 0 <= value < (1 << 128):
            raise OverflowError("u128 value out of range")

        low = value & 0xFFFFFFFFFFFFFFFF
        high = value >> 64

        if self._is_be:
            self.write(struct.pack(">QQ", high, low))
        else:
            self.write(struct.pack("<QQ", low, high))

    def f32(self, value: float) -> None:
        self.write(struct.pack(">f" if self._is_be else "<f", value))

    def f64(self, value: float) -> None:
        self.write(struct.pack(">d" if self._is_be else "<d", value))

    def bool(self, value: bool) -> None:
        self.write(b"\x01" if value else b"\x00")

    def byte(self, value: bytes | bytearray | int) -> None:
        if isinstance(value, int):
            self.u8(value)
        else:
            if len(value) != 1:
                raise ValueError("byte() requires exactly one byte")
            self.write(value)

    def bytes(self, value: bytes | bytearray | memoryview) -> None:
        self.write(value)

    def str(self, value: str, encoding: str = "utf-8", errors: str = "strict") -> None:
        self.write(value.encode(encoding, errors))

    def list(self, type: str, values: Iterable[int | float]) -> None:
        arr = array.array(type, values)

        if arr.itemsize > 1:
            need_swap = (self._is_be and sys.byteorder == "little") or (not self._is_be and sys.byteorder == "big")

            if need_swap:
                arr.byteswap()

        arr.tofile(self.file)
        self._size = None

    def none(self, size: int = 1) -> None:
        self.write(b"\x00" * size)

    @property
    def offset(self) -> int:
        return self.file.tell()

    @offset.setter
    def offset(self, offset: int) -> None:
        self.file.seek(offset)

    @property
    def size(self) -> int:
        if self._size is not None:
            return self._size

        offset = self.file.tell()
        self.file.seek(0, 2)
        self._size = self.file.tell()
        self.file.seek(offset)

        return self._size

    def align(self, padding: int = 4, offset: int = 0, value: int = 0) -> None:
        curr_offset = self.file.tell()
        mod = (curr_offset + offset) % padding

        if mod != 0:
            self.write(bytes([value]) * (padding - mod))

    def flush(self) -> None:
        if hasattr(self.file, "flush"):
            self.file.flush()

    def getvalue(self) -> bytes:
        if hasattr(self.file, "getvalue"):
            return self.file.getvalue()

        offset = self.file.tell()
        self.file.seek(0)
        data = self.file.read()
        self.file.seek(offset)
        return data

    def close(self) -> None:
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._is_temp_mode:
            self.file.close()
