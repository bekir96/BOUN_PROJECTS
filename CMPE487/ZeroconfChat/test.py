#!/usr/bin/env python3

import os
import sys

__password__ = ""

__dictCourses__ = {"EC206" : {"Days":"M,M", "Slots": "3,4", "Quota": 3, "Registered": 0 },
        "EC48T" : {"Days":"M,M,M", "Slots": "5,6,7", "Quota": 3, "Registered": 0 },
        "EC48J" : {"Days":"T,T,T", "Slots": "1,2,3", "Quota": 3, "Registered": 0 },
        "EC331" : {"Days":"W,W,W", "Slots": "5,6,7", "Quota": 3, "Registered": 0 },
        "EC481" : {"Days":"Th,Th", "Slots": "1,2", "Quota": 2, "Registered": 0 },
        "EC406" : {"Days":"Th,Th", "Slots": "3,4", "Quota": 2, "Registered": 0 },
        "EC48Z" : {"Days":"Th,Th,Th", "Slots": "5,6,7", "Quota": 2, "Registered": 0 },
        "EC381" : {"Days":"T,T", "Slots": "3,4", "Quota": 3, "Registered": 0 },
        "EC411" : {"Days":"W,W,W", "Slots": "4,5", "Quota": 3, "Registered": 0 },
        "EC350" : {"Days":"T,T,T", "Slots": "3,4,5", "Quota": 3, "Registered": 0 },
        }


__dictStudents__ = { "2015300000" : {"Name": "Ahmet", "GPA": 3.55, "Semester":7, "Department":"Economics", "Courses" : []}, 
        "2015300001" : {"Name": "Buse", "GPA": 2.72, "Semester":5, "Department":"Economics", "Courses" : []},
        "2015300002" : {"Name": "Can", "GPA": 3.14, "Semester":6, "Department":"Management", "Courses" : []},
        "2015300003" : {"Name": "Deniz", "GPA": 2.56, "Semester":6, "Department":"Political Science", "Courses" : []},
        "2015300004" : {"Name": "Emre", "GPA": 3.70, "Semester":8, "Department":"Economics", "Courses" : []}
        }

def show_profile():
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    print("\n\n\n  Student Id: " + "\033[0;27;46m " + __username__ + " \x1b[0m" + "\n")
    print("  Name: " + "\033[0;27;46m " + __dictStudents__[__username__]["Name"] + " \x1b[0m" + "\n")
    print("  GPA: " + "\033[0;27;46m " + str(__dictStudents__[__username__]["GPA"]) + " \x1b[0m" + "\n")
    print("  Semester: " + "\033[0;27;46m " + str(__dictStudents__[__username__]["Semester"]) + " \x1b[0m" + "\n")
    print("  Department: " + "\033[0;27;46m " + __dictStudents__[__username__]["Department"] + " \x1b[0m" + "\n")
    yellow_flag("[->]", "Press enter key to go main page...")


def course_list_preparation():
    os.system('clear')
    print("\n1. Add course\n")
    print("2. Drop course\n")
    print("\033[0;01;34m " + "\n\nType the selection you want to: " +  "\033[0;37;40m" , end = "")
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    __selection__ = input()
    try:
        val = int(__selection__)
        if val > 2 :
            red_flag("[!]","Please choose valid selection...")
            tmp = input()
            course_list_preparation()
        else :                                                        
            what_to_do(val)
    except ValueError:
        red_flag("[!]","Please choose valid selection...")
        tmp = input()
        course_list_preparation()

def what_to_do(val):
    if val == 1:
        print("\033[0;01;34m " + "\nPlease enter the course code you want to add: " +  "\033[0;37;40m" , end = "")
        sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
        __selection__ = input()
        while __selection__ not in __dictCourses__:
            print("\a \033[100F \033[2K \033[s \r" + "\033[0;01m " + "[!]" +  "  \033[0;37;41m " + str('Please write valid input. Enter to continue.') + " \x1b[0m" 
                                                                                    + "\033[1;30;41m" + "" + " \x1b[0m", end="")
            tmp = input()
            os.system('clear') 
            print("\033[0;01;34m " + "\nPlease enter the course code you want to add: " +  "\033[0;37;40m" , end = "")
            sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
            __selection__ = input()
        if __selection__ not in __dictStudents__[__username__]["Courses"]: 
            if __dictCourses__[__selection__]["Quota"] == __dictCourses__[__selection__]["Registered"]:
                print("\nThere is no quota!")
                yellow_flag("[->]","Press enter key to go main page...")
            elif (__selection__ == "EC48J" or __selection__ == "EC381" or __selection__ == "EC350"):
                if "EC48J" in __dictStudents__[__username__]["Courses"]: 
                    print("\nConflict with EC48J")
                    yellow_flag("[->]","Press enter key to go main page...")
                elif "EC381" in __dictStudents__[__username__]["Courses"]: 
                    print("\nConflict with EC381")
                    yellow_flag("[->]","Press enter key to go main page...")
                elif "EC350" in __dictStudents__[__username__]["Courses"]: 
                    print("\nConflict with EC350")
                    yellow_flag("[->]","Press enter key to go main page...")
                else:
                    __dictStudents__[__username__]["Courses"].append(__selection__)
                    __dictCourses__[__selection__]["Registered"] += 1
                    yellow_flag("[->]","Press enter key to go main page...", "(" + __selection__ + " is added to your schedule." + ")")
            elif (__selection__ == "EC331" or __selection__ == "EC411"):
                if "EC411" in __dictStudents__[__username__]["Courses"]: 
                    print("\nConflict with EC411")
                    yellow_flag("[->]","Press enter key to go main page...")
                elif "EC331" in __dictStudents__[__username__]["Courses"]: 
                    print("\nConflict with EC331")
                    yellow_flag("[->]","Press enter key to go main page...")
                else:
                    __dictStudents__[__username__]["Courses"].append(__selection__)
                    __dictCourses__[__selection__]["Registered"] += 1
                    yellow_flag("[->]","Press enter key to go main page...", "(" + __selection__ + " is added to your schedule." + ")")
            else:
                __dictStudents__[__username__]["Courses"].append(__selection__)
                __dictCourses__[__selection__]["Registered"] += 1
                yellow_flag("[->]","Press enter key to go main page...", "(" + __selection__ + " is added to your schedule." + ")")
        else:
            red_flag("[!]","Please choose valid course which is not added...") 
            tmp = input()
            what_to_do(val)
    else:          
        print("\033[0;01;34m " + "\nPlease enter the course code you want to drop: " +  "\033[0;37;40m" , end = "")
        sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
        __selection__ = input()
        while __selection__ not in __dictCourses__:
            print("\a \033[100F \033[2K \033[s \r" + "\033[0;01m " + "[!]" +  "  \033[0;37;41m " + str('Please write valid input. Enter to continue.') + " \x1b[0m" 
                                                                                    + "\033[1;30;41m" + "" + " \x1b[0m", end="")
            tmp = input()
            os.system('clear') 
            print("\033[0;01;34m " + "\nPlease enter the course code you want to drop: " +  "\033[0;37;40m" , end = "")
            sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
            __selection__ = input()
        if __selection__ in __dictStudents__[__username__]["Courses"]: 
            index = __dictStudents__[__username__]["Courses"].index(__selection__)
            del __dictStudents__[__username__]["Courses"][index]
            __dictCourses__[__selection__]["Registered"] -= 1
            yellow_flag("[->]","Press enter key to go main page...", "(" + __selection__ + " is dropped." + ")")

        else:
            red_flag("[!]","The course is NOT in your schedule. Please choose valid course which is added recently...") 
            tmp = input()
            os.system('clear')
            what_to_do(val)                                      

def courses_and_quotas():
    print("\033[0;01;34m " + "\nPlease enter the course code: " +  "\033[0;37;40m" , end = "")
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    __selection__ = input()
    while __selection__ not in __dictCourses__:
        print("\a \033[100F \033[2K \033[s \r" + "\033[0;01m " + "[!]" +  "  \033[0;37;41m " + str('Please write valid input. Enter to continue.') + " \x1b[0m" 
                                                                                + "\033[1;30;41m" + "" + " \x1b[0m", end="")
        tmp = input()
        os.system('clear') 
        print("\033[0;01;34m " + "\nPlease enter the course code: " +  "\033[0;37;40m" , end = "")
        sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
        __selection__ = input()

    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    print("\n\n\n  " + "\033[0;27;46m " + __selection__ + " \x1b[0m" + "\n")
    print("  Total Quota:" + "\033[0;27;46m " + str(__dictCourses__[__selection__]["Quota"]) + " \x1b[0m" + "\n")
    print("  Registered: " + "\033[0;27;46m " + str(__dictCourses__[__selection__]["Registered"]) + " \x1b[0m" + "\n")
    print("  Days: " + "\033[0;27;46m " + __dictCourses__[__selection__]["Days"] + " \x1b[0m" + "\n")
    print("  Hours: " + "\033[0;27;46m " + __dictCourses__[__selection__]["Slots"] + " \x1b[0m" + "\n")
    yellow_flag("[->]", "Press enter key to go main page...")
        

def my_schedule():
    dict_schedule ={"Monday":[],
                    "Tuesday":[],
                    "Wednesday":[],
                    "Thursday":[],
                    "Friday":[]
                }

    for items in __dictStudents__[__username__]["Courses"]:
        days, *tmp = __dictCourses__[items]["Days"].split(",")
        if days == "M":
            __tmp_string__ = items + "(" + __dictCourses__[items]["Slots"] + ")"
            dict_schedule["Monday"].append(__tmp_string__)
        if days == "T":
            __tmp_string__ = items + "(" + __dictCourses__[items]["Slots"] + ")"
            dict_schedule["Tuesday"].append(__tmp_string__)
        if days == "W":
            __tmp_string__ = items + "(" + __dictCourses__[items]["Slots"] + ")"
            dict_schedule["Wednesday"].append(__tmp_string__)
        if days == "Th":
            __tmp_string__ = items + "(" + __dictCourses__[items]["Slots"] + ")"
            dict_schedule["Thursday"].append(__tmp_string__)
        if days == "F":
            __tmp_string__ = items + "(" + __dictCourses__[items]["Slots"] + ")"
            dict_schedule["Friday"].append(__tmp_string__)                                   
        
    print("\n  Monday: " + str(dict_schedule["Monday"]))
    print("\n  Tuesday: " + str(dict_schedule["Tuesday"]))
    print("\n  Wednesday: " + str(dict_schedule["Wednesday"]))
    print("\n  Thursday: " + str(dict_schedule["Thursday"]))
    print("\n  Friday: " + str(dict_schedule["Friday"]))
    yellow_flag("[->]", "Press enter key to go main page...")



                

def green_flag(__punctuation__, __str__, __optional__=""):
    print("\033[100F \033[2K \033[s \r" + "\033[0;01m " + __punctuation__ +  "  \033[0;47;42m " + __str__ + " \x1b[0m" 
                                                                            + "\033[1;37;42m " + __optional__ + " \x1b[0m", end="")                


def yellow_flag(__punctuation__, __str__, __optional__=""):
    print("\033[100F \033[2K \033[s \r" + "\033[0;01m " + __punctuation__ +  "  \033[0;37;43m " + __str__ + " \x1b[0m" 
                                                                            + "\033[1;47;43m" + __optional__ + " \x1b[0m", end="")

def red_flag(__punctuation__, __str__, __optional__=""):
    print("\a \033[100F \033[2K \033[s \r" + "\033[0;01m " + __punctuation__ +  "  \033[0;37;41m " + __str__ + " \x1b[0m" 
                                                                            + "\033[1;30;41m" + __optional__ + " \x1b[0m", end="")

class Switcher(object):
    def indirect(self,i):
        __method_name__ = 'number_' + str(i)
        __method__ = getattr(self, __method_name__, lambda :'Invalid option')
        return __method__()

    def number_1(self):
        os.system('clear')
        course_list_preparation()
        tmp = input()
        os.system('clear')

    def number_2(self):
        os.system('clear')
        courses_and_quotas()
        tmp = input()
        os.system('clear')
        
    def number_3(self):
        os.system('clear')
        my_schedule()
        tmp = input()
        os.system('clear')

    def number_4(self):
        os.system('clear')
        show_profile()
        tmp = input()
        os.system('clear')

    def number_5(self):
        os.system('clear')
        main_page()

def console():
    os.system('clear')  
    green_flag("[->]","Welcome",__dictStudents__[__username__]["Name"] )
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    __header__ = "SELECTION"
    print("\n\n")
    print(__header__.center(48, ' '))
    print('=' * 48)
    print('| {0:s}  {1:s}|'.format("1)".ljust(17), "Course List Preparation".ljust(26)))
    print('| {0:s}  {1:s}|'.format("2)".ljust(17), "Courses and Quotas".ljust(26)))
    print('| {0:s}  {1:s}|'.format("3)".ljust(17), "My Schedule".ljust(26)))
    print('| {0:s}  {1:s}|'.format("4)".ljust(17), "My Account Information".ljust(26)))
    print('| {0:s}  {1:s}|'.format("5)".ljust(17), "Logout".ljust(26)))
    print('=' * 48)
    
    print("\033[0;01;34m " + "\n\nType the selection you want to: " +  "\033[0;37;40m" , end = "")
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    __selection__ = input()
    try:
        val = int(__selection__)
        if val > 6 :
            red_flag("[!]","Please choose valid selection...")
            tmp = input()
        else :                                                        
            s = Switcher()
            s.indirect(__selection__)
    except ValueError:
        red_flag("[!]","Please choose valid selection...")
        tmp = input()


def main_page():
    os.system('clear') 
    print("\n--- Welcome to BOUN REGISTRATION ---\n")
    print("1. Login")
    print("2. Exit\n")
    print("\033[0;01;34m " + "\nType the selection you want to: " +  "\033[0;37;40m" , end = "")
    sys.stdout.write('\x1b[1;34m' + "" + '\x1b[0m')
    __selection__ = input()
    try:
        val = int(__selection__)
        if val > 2 :
            red_flag("[!]","Please choose valid selection...")
            tmp = input()
            main_page()
        else :
            if val == 1:
                global __username__
                __username__ = input("User Name: ") 
                while __username__ not in __dictStudents__:
                    print("\a \033[100F \033[2K \033[s \r" + "\033[0;01m " + "[!]" +  "  \033[0;37;41m " + str('Please write valid input. Enter to continue.') + " \x1b[0m" 
                                                                                            + "\033[1;30;41m" + "" + " \x1b[0m", end="")
                    tmp = input()
                    os.system('clear') 
                    print("\n")
                    __username__ = input("User Name: ") 
                print("\n")
                __password__ = input("Password: ")
                while True:
                    console()                                                                     
            else:
                sys.exit(0)
    except ValueError:
        red_flag("[!]","Please choose valid selection...")
        tmp = input()
        main_page()

main_page()
