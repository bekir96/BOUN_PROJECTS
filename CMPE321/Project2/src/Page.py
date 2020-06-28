import sys
import os
import os.path
from pathlib import Path
import stat

from Containers import *
from File import *
import ctypes

class Page:
    @staticmethod
    def findStatus(page: str, offset: int) -> bool:
        byte_page = bytearray(page)
        status: bool = bool.from_bytes(byte_page[offset:offset+1],"big")
        return status

    @staticmethod
    def findInteger(page: str, offset: int) -> int:
        byte_page = bytearray(page)
        value: int = int.from_bytes(byte_page[offset:offset+4], "big")
        return value

    @staticmethod 
    def findString(page: str, offset: int, size: int) -> str:
        byte_page = bytearray(page)
        value: str = ''
        for i in range(0,size):
            c: str = byte_page[offset+i:offset+i+1].decode('cp1250')
            if c == '\0': 
                break
            value += c
        return value

    @staticmethod
    def findType(page: str, number: int) -> Optional[Type]:
        offset: int = SYSTEM_CATALOGUE_PAGE_HEADER_SIZE + number * SYSTEM_CATALOGUE_RECORD_SIZE
        temp: Type = Type()
        temp.name = Page.findString(page, offset, SYSTEM_CATALOGUE_RECORD_NAME_SIZE)
        temp.numberOfFields = Page.findInteger(page, offset + 10)
        temp.isDeleted = Page.findStatus(page, offset + 14)
        temp.isExist = Page.findStatus(page, offset + 15)
        temp.fieldNames = [None] * temp.numberOfFields

        cursor:int
        for i in range(0,temp.numberOfFields):
            cursor = SYSTEM_CATALOGUE_RECORD_HEADER_SIZE + i * SYSTEM_CATALOGUE_RECORD_FIELD_NAME_SIZE
            temp.fieldNames[i] = Page.findString(page, offset + cursor, SYSTEM_CATALOGUE_RECORD_FIELD_NAME_SIZE)
        return temp

    @staticmethod
    def findTypeByName(name: str) -> Optional[Type]:
        temp: Type = Type()
        buffer: str
        cursor: int
        for i in range(0, MAX_PAGE_PER_FILE):
            buffer = File.getPage(SYSTEM_CATALOGUE_FILE_NAME, FILE_HEADER_SIZE + i * PAGE_SIZE)
            for j in range(0, SYSTEM_CATALOGUE_MAX_RECORD_PER_PAGE):
                cursor = SYSTEM_CATALOGUE_PAGE_HEADER_SIZE + j * SYSTEM_CATALOGUE_RECORD_SIZE
                controlName: str = Page.findString(buffer, cursor, SYSTEM_CATALOGUE_RECORD_NAME_SIZE)
                isDeleted: bool = Page.findStatus(buffer, cursor + SYSTEM_CATALOGUE_RECORD_NAME_SIZE + 4)
                if controlName == name and not isDeleted:
                    temp = Page.findType(buffer, j)
                    return temp
        return None

    @staticmethod
    def findRecord(page: str, number: int, name: str) -> Optional[Record]:
        offset: int = DATA_FILE_PAGE_HEADER_SIZE + number * DATA_FILE_RECORD_SIZE
        temp: Record = Record()
        temp.name = name
        temp.isDeleted = Page.findStatus(page, offset)
        temp.isExist = Page.findStatus(page, offset+1)
        temp.numberOfFields = Page.findTypeByName(name).numberOfFields
        temp.fieldValues = [None] * temp.numberOfFields
        for i in range(0, temp.numberOfFields):
            temp.fieldValues[i] = Page.findInteger(page, offset + DATA_FILE_RECORD_HEADER_SIZE + i*4)

        return temp

    @staticmethod
    def putInteger(page: str, offset: int, value: int) -> str:
        byte_page = bytearray(page)
        byte_page[offset:offset+4] = (value).to_bytes(4, byteorder="big", signed=True)
        return byte_page

    @staticmethod
    def putString(page: str, offset: int, name: str, size: int) -> str:
        c: str
        byte_page: bytearray = bytearray(page)
        for i in (range(0,size) and range(0, len(name))):
            c = name[i]
            byte_page[offset+i:offset+i+1] = c.encode('cp1250')
        if size != len(name):
            byte_page[offset+i+1:offset+i+2] = '\0'.encode('cp1250')
        return byte_page

    @staticmethod
    def putStatus(page: str, offset: int, value: bool) -> str:
        byte_page = bytearray(page)
        byte_page[offset:offset+1] = value.to_bytes(1,"big")
        return byte_page

    @staticmethod
    def putType(page: str, number: int, type: Type) -> str:
        offset = SYSTEM_CATALOGUE_PAGE_HEADER_SIZE + number * SYSTEM_CATALOGUE_RECORD_SIZE
        page = Page.putString(page, offset, type.name, SYSTEM_CATALOGUE_RECORD_NAME_SIZE)
        page = Page.putInteger(page, offset + SYSTEM_CATALOGUE_RECORD_NAME_SIZE, type.numberOfFields)
        page = Page.putStatus(page, offset + SYSTEM_CATALOGUE_RECORD_NAME_SIZE + 4, type.isDeleted)
        page = Page.putStatus(page, offset + SYSTEM_CATALOGUE_RECORD_NAME_SIZE + 5, type.isExist)

        cursor: int
        for i in range(0, type.numberOfFields):
            cursor = SYSTEM_CATALOGUE_RECORD_HEADER_SIZE + i * SYSTEM_CATALOGUE_RECORD_FIELD_NAME_SIZE
            page = Page.putString(page, offset + cursor, type.fieldNames[i], SYSTEM_CATALOGUE_RECORD_FIELD_NAME_SIZE)
        
        return page

    @staticmethod
    def putRecord(page: str, number: int, record: Record) -> str:
        offset = DATA_FILE_PAGE_HEADER_SIZE + number * DATA_FILE_RECORD_SIZE
        page = Page.putStatus(page, offset, record.isDeleted)
        page = Page.putStatus(page, offset+1, record.isExist)
        record.numberOfFields = Page.findTypeByName(record.name).numberOfFields
        for i in range(0,record.numberOfFields):
            page = Page.putInteger(page, offset + DATA_FILE_RECORD_HEADER_SIZE + i*4, record.fieldValues[i])
        
        return page

    @staticmethod
    def assign(o1: Record) -> Optional[Record]:
        record: Record = Record()
        record.name = o1.name
        record.isDeleted = o1.isDeleted
        record.isExist = o1.isExist
        record.numberOfFields = o1.numberOfFields
        record.fieldValues = o1.fieldValues
        return record