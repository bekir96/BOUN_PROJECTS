from Containers import *
from Page import *
import os

class File:
    @staticmethod
    def getPage(filename: str, offset: int) -> str:
        f:file = open(filename, 'rb')
        f.seek(offset, 0)
        buffer = f.read(PAGE_SIZE)
        f.close()
        return buffer

    @staticmethod
    def putPage(filename: str, offset: int, pageContent: str) -> None:
        f:file = open(filename, 'rb+')
        f.seek(offset, 0)
        f.write(pageContent)
        f.close()

    @staticmethod
    def existFile(filename: str) -> bool:
        pathname: Path = Path(filename)
        if pathname.is_file():
            return True
        else:
            return False

    @staticmethod
    def initializeFile(filename: str) -> None:
        f = open(filename, "wb")
        f.seek(MAX_FILE_SIZE-1, 0)
        f.write(b"\0")
        f.close()

        for i in range(0, MAX_PAGE_PER_FILE):
            buffer: str = File.getPage(filename, FILE_HEADER_SIZE + i * PAGE_SIZE)
            buffer = bytearray(buffer)
            buffer[0:4] = (i).to_bytes(4, byteorder="big", signed=True)
            # buffer = Page.putInteger(buffer, 0, i)
            File.putPage(filename, FILE_HEADER_SIZE + i * PAGE_SIZE, buffer)