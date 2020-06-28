from Containers import *
from Storage import *

class Switcher(object):
    def indirect(self, operation: str, info: list):
        method_name = operation
        method = getattr(self, method_name, lambda :'Invalid option')
        return method(info)

    def createtype(self, info: list):
        type: Type = Type()
        type.name = info[0]
        type.numberOfFields = int(info[1])
        type.fieldNames = info[2:]
        storage.createType(type)

    def deletetype(self, info: list):
        storage.deleteType(info[0])
        
    def listtype(self, info: list):
        type_list: List[Type] = []
        type_list = storage.listType()
        if type_list == []:
            return

        type_list.sort(key=lambda type: type.name, reverse=False)
        print_list = (type.name for type in type_list)
        print_str.append('\n'.join(map(str, print_list)))

    def createrecord(self, info: list):
        record: Record = Record()
        record.name = info[0]
        record.fieldValues = list(map(int, info[1:]))
        storage.createRecord(record)

    def deleterecord(self, info: list):
        storage.deleteRecord(info[0], int(info[1]))

    def updaterecord(self, info: list):
        record: Record = Record()
        record.name = info[0]
        record.fieldValues = list(map(int, info[1:]))
        storage.updateRecord(record)

    def searchrecord(self, info: list):
        record: Record = Record()
        record = storage.searchRecord(info[0], int(info[1]))
        if record is None:
            return

        print_str.append(' '.join(map(str, record.fieldValues)))

    def listrecord(self, info: list):
        record_list: List[Record] = []
        record_list = storage.listRecord(info[0])
        if record_list == [] or record_list == None:
            return

        record_list.sort(key=lambda record: record.fieldValues[0], reverse=False)
        print_list = (' '.join(map(str, record.fieldValues)) for record in record_list)
        print_str.append('\n'.join(map(str, print_list)))


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Run with the following: \n program.exe $input_path $output_path")
        sys.exit(0)
 
    if not File.existFile(sys.argv[1]):
        print("invalid input file for open: " + sys.argv[1])
        sys.exit(0)

    print_str: list = []
    storage = Storage()
    input_file: str = open(sys.argv[1], 'r')
    output_file: str = open(sys.argv[2], 'w+')
    
    for line in input_file:
        o1, o2, *info = " ".join(line.split()).replace('\n','').split(" ")
        operation: str = o1 + o2
        s = Switcher()
        s.indirect(operation, info)

    output_file.write('\n'.join(map(str, print_str)))