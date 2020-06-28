## Storage Manager System

### Project Description

A storage manager is a program that controls how the memory will be used to save data to increase the efficiency of a system. The storage manager translates the various DML statements into low-level file-system commands. Thus, the storage manager is responsible for storing, retrieving, and updating data in the database. Can be thought as the interface between the DBMS and all the "physically" at the low levels. Storage manager is responsible for retrieving a record, and the other parts of the DBMS are only concerned with the records, not with files, pages, disk and so on. In this project, I am expected to design a storage manager system that supports DDL and DML operations. There should be a system catalogue which stores metadata and multiple data files that store the actual data. 

### How to Run

Use `python3 2014400054/src/storageManager.py <inputFile> <outputFile>`  command. 

### Operations

* DDL Operations

| Operation | Input Format                                                   | Output Format                                                |
| --------- | -------------------------------------------------------------  | ------------------------------------------------------------ |
| Create    | create type \<type_name> \<number_of_fields> \<field1_name> ...| None                                                         |
| Delete    | delete type \<type_name>                                       | None                                                         |
| List      | list type                                                      | \<type1_name><br />\<type2_name><br />...                    |

* DML Operations

| Operation | Input Format                                                      | Output Format                                                |
| --------- | ----------------------------------------------------------------- | ------------------------------------------------------------ |
| Create    | create record \<type_name> \<field1_value> \<field2-value>...     |  None                                                        |
| Delete    | delete record \<type_name> \<primary_key>                         |  None                                                        |
| Search    | search record \<type_name> \<primary_key>                         | \<field1_value>\<field2_value>...                            |           
| Update    | update record \<type_name> \<primary_key> \<field1_value> ...     |  None                                                        |
| List      | list record \<type_name>                                          | \<record1.field1_value>\<record1.field2_value>...<br />\<record2.field1_value>\<record2.field2_value>...<br />...|

### File Structure

Output, system catalogue and meta data file are in "txt" format and last two item are written as binary data format.




