from Constraints import *
from Page import *
from File import *

class Storage:
    def __init__(self):
        if File.existFile(SYSTEM_CATALOGUE_FILE_NAME):
            return
        else:
            File.initializeFile(SYSTEM_CATALOGUE_FILE_NAME)
    

    def createType(self, type: Type) -> None:
        if Page.findTypeByName(type.name) is not None:
            return

        temp: Type = Type()

        for i in range(0, MAX_PAGE_PER_FILE):
            buffer = self.getPage(SYSTEM_CATALOGUE_FILE_NAME,i)
            type_number = Page.findInteger(buffer, 4)

            if type_number != SYSTEM_CATALOGUE_MAX_RECORD_PER_PAGE:
                for j in range(0, type_number):
                    temp = Page.findType(buffer, j)

                    if temp.name == type.name and temp.isDeleted:
                        buffer = Page.putType(buffer, j, type)
                        self.putPage(SYSTEM_CATALOGUE_FILE_NAME, i, buffer)
                        return
                        
                for j in range(type_number, SYSTEM_CATALOGUE_MAX_RECORD_PER_PAGE):
                    buffer = Page.putType(buffer, j, type)
                    buffer = Page.putInteger(buffer, 4, type_number + 1)
                    self.putPage(SYSTEM_CATALOGUE_FILE_NAME, i, buffer)
                    return


    def deleteType(self, name: str) -> None:
        i = 0
        file: str = '{}_{}.txt'.format(name, str(i))
        while File.existFile(file):
            os.remove(file)
            i+=1
        
        buffer: str
        temp: Type = Type()

        for i in range(0, MAX_PAGE_PER_FILE):
            buffer = self.getPage(SYSTEM_CATALOGUE_FILE_NAME, i)
            type_number = Page.findInteger(buffer, 4)
            if type_number == 0:
                return

            for j in range(0, type_number):
                temp = Page.findType(buffer, j)
                if temp.name == name and not temp.isDeleted and temp.isExist:
                    temp.isDeleted = True
                    buffer = Page.putType(buffer, j, temp)
                    self.putPage(SYSTEM_CATALOGUE_FILE_NAME, i, buffer)
                    return


    def listType(self) -> Optional[List[Type]]:
        type_list: List[Type] = []
        temp: Type = Type()
        buffer: str 
        
        for i in range(0, MAX_PAGE_PER_FILE):
            buffer = self.getPage(SYSTEM_CATALOGUE_FILE_NAME, i)
            type_number = Page.findInteger(buffer, 4)

            for j in range(0, type_number):
                temp = Page.findType(buffer, j)

                if not temp.isDeleted and temp.isExist:
                    type_list.append(temp)

        return type_list


    def createRecord(self, record: Record) -> None:
        if Page.findTypeByName(record.name) is None:
            return

        self.binarySort(0, record, 0)

    def binarySort(self, pageID: int, record: Record, fileno: int) -> None: 
        filename = '{}_{}.txt'.format(record.name, str(fileno))
        if not File.existFile(filename):
            self.createDataFile(filename, record)
            return

        buffer = self.getPage(filename, pageID)
        record_number = Page.findInteger(buffer, 4)

        current: int = self.binarySearch(buffer, 0, record_number-1, record.fieldValues[0], record.name)
        next: Record = Record()

        while current < record_number:
            next = Page.findRecord(buffer, current, record.name)
            buffer = Page.putRecord(buffer, current, record)
            self.putPage(filename, pageID, buffer)
            current+=1
            record = Page.assign(next)
        
        if current == DATA_FILE_MAX_RECORD_PER_PAGE:
            if pageID == MAX_PAGE_PER_FILE-1:
                self.binarySort(0, record, fileno+1)
            else:
                self.binarySort(pageID+1, record, fileno)
            return
        else:
            self.putFileHeader(filename, 1)
            buffer = Page.putInteger(buffer, 4, record_number+1)
            buffer = Page.putRecord(buffer, current, record)
            self.putPage(filename, pageID, buffer)

    def binarySearch(self, page: str, l: int, r: int, key: int, name: str) -> int: 
        record: Record = Record()
        while l <= r: 
            mid = l + (r - l) // 2; 
            record = Page.findRecord(page, mid, name)

            if record.fieldValues[0] == key: 
                return mid 
            elif record.fieldValues[0] < key: 
                l = mid + 1
            else: 
                r = mid - 1
        return l
    

    def deleteRecord(self, name: str, key: int) -> None:
        if Page.findTypeByName(name) is None:
            return

        buffer: str
        file_header: str
        i: int = 0
        filename:  str = '{}_{}.txt'.format(name, str(i))
        record: Record = Record()

        while File.existFile(filename):
            for j in range(0, MAX_PAGE_PER_FILE):
                buffer = self.getPage(filename, j)
                record_number = Page.findInteger(buffer, 4)

                for k in range(0, record_number):
                    record = Page.findRecord(buffer, k, name)
                    record_key: int = record.fieldValues[0]

                    if record_key == key and not record.isDeleted and record.isExist:
                        record.isDeleted = True
                        buffer = Page.putRecord(buffer, k, record)
                        self.putPage(filename, j, buffer)
                        self.putFileHeader(filename, -1)
                        file_header = self.getFileHeader(filename)
                        number = Page.findInteger(file_header, 0)

                        if number == 0:
                            os.remove(filename)
                        return
            i+=1
            filename = '{}_{}.txt'.format(name, str(i))

        

    def updateRecord(self, record: Record) -> None:
        if self.searchRecord(record.name, record.fieldValues[0]) is None:
            return

        buffer: str
        i: int = 0
        filename:  str = '{}_{}.txt'.format(record.name, str(i))
        key: int = record.fieldValues[0]
        temp: Record = Record()

        while File.existFile(filename):
            for j in range(0, MAX_PAGE_PER_FILE):
                buffer = self.getPage(filename, j)
                record_number = Page.findInteger(buffer, 4)

                for k in range(0, record_number):
                    temp = Page.findRecord(buffer, k, record.name)
                    temp_key: int = temp.fieldValues[0]

                    if temp_key == key and not temp.isDeleted and temp.isExist:
                        buffer = Page.putRecord(buffer, k, record)
                        self.putPage(filename, j, buffer)
                        return
            i+=1
            filename = '{}_{}.txt'.format(record.name, str(i))


    def searchRecord(self, name: str, key: int) -> Optional[Record]:
        if Page.findTypeByName(name) is None:
            return None

        buffer: str
        i: int = 0
        filename:  str = '{}_{}.txt'.format(name, str(i))
        record: Record = Record()

        while File.existFile(filename):
            for j in range(0, MAX_PAGE_PER_FILE):
                buffer = self.getPage(filename, j)
                record_number = Page.findInteger(buffer, 4)

                for k in range(0, record_number):
                    record = Page.findRecord(buffer, k, name)
                    record_key: int = record.fieldValues[0]

                    if record_key == key and not record.isDeleted and record.isExist:
                        return record
            i+=1
            filename = '{}_{}.txt'.format(name,str(i))

        return None

    
    def listRecord(self, name: str) -> Optional[List[Record]]:
        if Page.findTypeByName(name) is None:
            return None

        record_list: List[Record] = []
        buffer: str
        i: int = 0
        filename:  str = '{}_{}.txt'.format(name, str(i))
        record: Record = Record()
        
        while File.existFile(filename):
            for j in range(0, MAX_PAGE_PER_FILE):
                buffer = self.getPage(filename, j)
                record_number = Page.findInteger(buffer, 4)

                for k in range(0, record_number):
                    record = Page.findRecord(buffer, k, name)

                    if not record.isDeleted and record.isExist:
                        record_list.append(record)
            i+=1
            filename = '{}_{}.txt'.format(name, str(i))

        return record_list


    def getPage(self, filename: str, pageID: int) -> str:
        return File.getPage(filename, FILE_HEADER_SIZE + pageID * PAGE_SIZE)

    def putPage(self, filename: str, pageID: int, pageContent: str) -> None:
        File.putPage(filename, FILE_HEADER_SIZE + pageID * PAGE_SIZE, pageContent)

    def getFileHeader(self, filename:str) -> str:
        f:file = open(filename, 'rb')
        f.seek(0, 0)
        buffer = f.read(4)
        f.close()
        return buffer

    def putFileHeader(self, filename: str, summation: int) -> None:
        file_header = self.getFileHeader(filename)
        number = Page.findInteger(file_header, 0)
        file_header = Page.putInteger(file_header, 0, number + summation)
        f:file = open(filename, 'rb+')
        f.seek(0, 0)
        f.write(file_header)
        f.close()

    def createDataFile(self, filename: str, record: Record) -> None:
        File.initializeFile(filename)
        buffer = self.getPage(filename, 0)
        buffer = Page.putRecord(buffer, 0, record)
        buffer = Page.putInteger(buffer, 4, 1)
        self.putPage(filename, 0, buffer)
        self.putFileHeader(filename, 1)

# a = Storage()


# # type = Type()
# # type.name = "deneme"
# # type.numberOfFields = 3
# # type.fieldNames = ["name", "age", "species"]
# # a.createType(type)

# # record = Record()
# # record.name = "deneme"

# # for i in range(0, MAX_PAGE_PER_FILE * DATA_FILE_MAX_RECORD_PER_PAGE):
# #     record.fieldValues = [i, i, i]
# #     a.createRecord(record)

# buffer = a.getFileHeader("deneme_0.txt")
# buffer = bytearray(buffer)
# print(buffer)
# print("-"*50)

# buffer = a.getPage("deneme_0.txt", 0)
# buffer = bytearray(buffer)
# print(buffer)
# print("-"*50)

# buffer = a.getPage("deneme_1.txt", 0)
# buffer = bytearray(buffer)
# print(buffer)

