#!/usr/bin/env python
# -*- coding: latin-1 -*-

import re
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup

deps = [('ASIA', 'ASIAN+STUDIES'), ('ASIA', 'ASIAN+STUDIES+WITH+THESIS'), ('ATA', 'ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY'),('AUTO', 'AUTOMOTIVE+ENGINEERING'),('BM', 'BIOMEDICAL+ENGINEERING'),
        ('BIS', 'BUSINESS+INFORMATION+SYSTEMS'),('CHE', 'CHEMICAL+ENGINEERING'),('CHEM','CHEMISTRY'), ('CE', 'CIVIL+ENGINEERING'),('CET', 'COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY'),
        ("CMPE", "COMPUTER+ENGINEERING"), ('COGS', 'COGNITIVE+SCIENCE'),('CSE', 'COMPUTATIONAL+SCIENCE+%26+ENGINEERING'), ('CCS', 'CRITICAL+AND+CULTURAL+STUDIES'),('CEM', 'CONSTRUCTION+ENGINEERING+AND+MANAGEMENT'),
        ('INT', 'CONFERENCE+INTERPRETING'),('EQE', 'EARTHQUAKE+ENGINEERING'),('EC', 'ECONOMICS'), ('EF', 'ECONOMICS+AND+FINANCE'),('ED', 'EDUCATIONAL+SCIENCES'),
        ('CET', 'EDUCATIONAL+TECHNOLOGY'),('ETM', 'ENGINEERING+AND+TECHNOLOGY+MANAGEMENT'),('ENV', 'ENVIRONMENTAL+SCIENCES'), ('EE', 'ELECTRICAL+%26+ELECTRONICS+ENGINEERING'),
        ('ENVT','ENVIRONMENTAL+TECHNOLOGY'),('XMBA','EXECUTIVE+MBA'),('FE','FINANCIAL+ENGINEERING'),('PA','FINE+ARTS'),('FLED','FOREIGN+LANGUAGE+EDUCATION'),
        ('GED','GEODESY'),('GPH','GEOPHYSICS'),('GUID','GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING'),('HIST','HISTORY'),('HUM','HUMANITIES+COURSES+COORDINATOR'),
        ('IE','INDUSTRIAL+ENGINEERING'),('INCT','INTERNATIONAL+COMPETITION+AND+TRADE'),('MIR','INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST'),
        ('MIR','INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS'),('INTT','INTERNATIONAL+TRADE'),('INTT','INTERNATIONAL+TRADE+MANAGEMENT'),('LS','LEARNING+SCIENCES'),
        ('LING','LINGUISTICS'),('AD','MANAGEMENT'), ('MATH','MATHEMATICS'),('SCED','MATHEMATICS+AND+SCIENCE+EDUCATION'),('MIS','MANAGEMENT+INFORMATION+SYSTEMS'),
        ('ME','MECHANICAL+ENGINEERING'),('MECA','MECHATRONICS+ENGINEERING'), ('BIO','MOLECULAR+BIOLOGY+%26+GENETICS'),('PHIL','PHILOSOPHY'),('PE','PHYSICAL+EDUCATION'),('PHYS','PHYSICS'),
        ('POLS','POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS'),('PRED','PRIMARY+EDUCATION'),('PSY','PSYCHOLOGY'),('YADYOK','SCHOOL+OF+FOREIGN+LANGUAGES'),
        ('SCED','SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION'),('SPL','SOCIAL+POLICY+WITH+THESIS'),('SOC','SOCIOLOGY'),('SWE','SOFTWARE+ENGINEERING'),
        ('SWE','SOFTWARE+ENGINEERING+WITH+THESIS'),('TRM','SUSTAINABLE+TOURISM+MANAGEMENT'),('SCO','SYSTEMS+%26+CONTROL+ENGINEERING'),('TRM','TOURISM+ADMINISTRATION'),
        ('WTR','TRANSLATION'),('TR','TRANSLATION+AND+INTERPRETING+STUDIES'),('TK','TURKISH+COURSES+COORDINATOR'),('TKL','TURKISH+LANGUAGE+%26+LITERATURE'),
         ('LL', 'WESTERN+LANGUAGES+%26+LITERATURES')]

deps.sort()

#Function that takes a sting as input and removes the "space" characters from it.
#This function returns the "space"less version of the input string.
def removeSpaces(string): 
        list = [] 
        for i in range(len(string)): 
                if string[i] != ' ': 
                        list.append(string[i]) 
        return toString(list) 

#Function that takes a list as input and returns a string that is formed by joining the elements of the list.
#It is basically used as a "list to string" converter.
def toString(List): 
        return ''.join(List)

#Function that takes a string as input returns the version of that string without certain character.
def removeAll(string):
        #list is the list version of the output string
        list = [] 
        for i in range(len(string)): 
                #If '+', '%', '3', '2', 'c', 'a', '6' and ' ' are not seen, the current character is added to the list.	
                if string[i] != '+' and string[i] != '%' and string[i] != '3' and string[i] != '2' and string[i] != 'c' and string[i] != 'a' and string[i] != '6' and  string[i] != ' ': 
                        list.append(string[i])
                #If '+' is seen, it is replaced by ' ' (space).	
                elif string[i] == '+' :
                        list.append(' ')
                #If '%', '2' and '6' are seen consecutively, they are replaced by '&'.
                elif string[i] == '%' and  string[i+1] == '2' and string[i+2] == '6':
                        list.append('&')
                #If '%', '3' and 'a' are seen consecutively, they are replaced by ';'.
                elif string[i] == '%' and  string[i+1] == '3' and string[i+2] == 'a':
                        list.append(';')
                #If '%', '2' and 'c' are seen consecutively, they are replaced by ','.
                elif string[i] == '%' and  string[i+1] == '2' and string[i+2] == 'c':
                        list.append(',')
        return toString(list) 

#Function that forms the required URL given the year and semester and pulls the data from that URL.
def get_data(year, semester, departmentshort="CMPE", departmentlong="COMPUTER+ENGINEERING"):
        #If the semester is Fall, there is a '-1' after "(year)/(year+1)"
        if semester == "Fall":
                url = 'https://registration.boun.edu.tr/scripts/sch.asp?donem=' + str(year) + '/' + str(int(year)+1) + '-1&kisaadi='+departmentshort+'&bolum='+departmentlong
        #If the semester is Fall, there is a '-2' after "(year-1)/(year)" in the URL
        elif semester == 'Spring':
                url = 'https://registration.boun.edu.tr/scripts/sch.asp?donem=' + str(year-1) + '/' + str(int(year)) + '-2&kisaadi='+departmentshort+'&bolum='+departmentlong
        #If the semester is Summer, there is a '-3' after "(year-1)/(year)" in the URL
        else : 
                url = 'https://registration.boun.edu.tr/scripts/sch.asp?donem=' + str(year-1) + '/' + str(int(year)) + '-3&kisaadi='+departmentshort+'&bolum='+departmentlong

        #BeautifulSoup is used to get the data from the URL
        req = requests.get(url, timeout=5)
                               
        soup = BeautifulSoup(req.text, 'html.parser')
        #find method is used to find the table tag with "border="1"" in it. This is the part of the HTML file with the table of information
        table = soup.find('table', {'border' : '1'})

        #data is a dictionary that stores instructors in courseno, coursename) keys
        data = {}
        #find_all returns a list containing all <tr class="schtd2"> and <tr class="schtd"> tags 
        for tr in table.find_all('tr', {'class' : ['schtd2', 'schtd'] }):
                #since some courses have lab sessions, we must check the length of tr["class"]
		#if the length is more than 1, it means that there are labs and we should ignore them by "continue"
                if len(tr["class"])>1:
                        continue
                #first <td> tag contains the course code
                courseno = tr.find_all('td')[0].text.strip()
                courseno, temp = courseno.split(".")
                courseno = removeSpaces(courseno)
                #third <td> tag contains the course name
                coursename = tr.find_all('td')[2].text.strip()
                #sixth <td> tag contains the instructor name
                instructor = tr.find_all('td')[5].text.strip()

                #Fills "data" according to the obtained information
                key = (courseno, coursename)
                #if there is no such key, create and store the instructor
                if key not in data :
                        data[key] = [instructor]
                #if there already is a key, and if instructor is not already in the dictionary, append the instructor
                elif instructor not in data[key]:
                        data[key].append(instructor)
        #Returns all collected data
        return data

#inp1 is the starting semester.
#Year and semester name are separated with a "-"
inp1 = sys.argv[1]
year1, semester1 = inp1.split("-")
#inp2 is the ending semester.
#Year and semester name are separated with a "-"
inp2 = sys.argv[2]
year2, semester2 = inp2.split("-")
#there are 3 possible semesters 
semesters = ['Spring', 'Summer', 'Fall']

#Function that returns "true" if there is at least 1 true value in the input list
def boolean(List) :
        sum = False
        for i in List :
                sum = sum or i
        return sum

def recursive(year1, semester1, year2, semester2, deps) :
        #dictionary that stores all departments
        courseList = {}
        #key name that help find the instructors
        key = 'I'
        for dep in deps:
                #this part is to initialize variables

                allCoursesDep = {}
                #number of undergrad courses
                allCoursesDep['U'] = 0
                #number of grad courses
                allCoursesDep['G'] = 0
                #stores the course names
                allCoursesDep['Course'] = [None]
                #stores the instructors
                allCoursesDep[key] = [None]

                #stores the U value in a semester
                semester_U = 0
                #stores the G value in a semester
                semester_G = 0
                #stores all the semesters in a year (in the required range)
                yearList = {}
                checker2 = True
                checker3 = True

                #boolean variable that checks the starting year and semester of the range
                checkSemester1 = False
                #boolean variable that checks the ending year and semester of the range
                checkSemester2 = False
                #variable to check the finishing of the range
                a = 1
                #list that stores the existance values of courses
                existList = []
                for year in range(int(year1), int(year2)+1):
                        semesterList = {}      
                        for semester in semesters :
                                semesterL = {}
                                semesterL['U'] = 0
                                semesterL['G'] = 0
                                if year == int(year1) and semester == semester1 :
                                        checkSemester1 = True
                                if year == int(year2) and semester == semester2 :
                                        checkSemester2 = True
                                if checkSemester1 == True and a < 2 :
                                        #tries to pull the data
                                        try:    
                                                data = get_data(year, semester, dep[0], dep[1])
                                                exist = True
                                                existList.extend([exist])
                                                if checkSemester2 == True :
                                                        a +=1
                                        #if it fails, handles the except	
                                        except:
                                                exist = False
                                                existList.extend([exist])
                                                if checkSemester2 == True :
                                                        a +=1
                                                continue
                                        #checker1 checks if there is any data in semesterL 
                                        checker1 = True
                                        #for all courses in data (ex: course= cmpe150 intro to..., course= cmpe160 intro to...)
                                        for course in data :
                                                try:
                                                        #course[0]= yearList
                                                        courseTemp = removeSpaces(course[0])
                                                        #finds the first integer value in a given string
                                                        index = re.search("\d", str(courseTemp))
                                                except:
                                                        exist = False
                                                        continue

                                                #in this for loop, U G and I values are calculated for the semesterL dictionary
                                                #x=instructors
                                                for x in data[course] :
                                                        #true if x is not "staff staff" 
                                                        checkStaff = True
                                                        if checker1 == True  :
                                                                checker1 = False
                                                                #if x=staff staff, writes false to the corresponding part of the dictionary
                                                                if x == 'STAFF STAFF' :
                                                                        checkStaff = False
                                                                        semesterL[key] = [[x],checkStaff]
                                                                #else writes true 
                                                                else :
                                                                        semesterL[key] = [[x],checkStaff]
                                                        
                                                        #if the instructor is not already in the dictionary, append
                                                        elif x != 'STAFF STAFF' and x not in semesterL[key][0]  :
                                                                semesterL[key][0].append(x)
                                                # if course code starts with a number smaller than 4, it is an undergrad course 
                                                if int(courseTemp[index.start()]) <= 4 :
                                                        semesterL['U'] += 1
                                                # if course code starts with a number larger than 4, it is an grad course 
                                                else :
                                                        semesterL['G'] += 1
                                                #while looking at instructors, it checks once if the instructor is already in allCoursesDep
                                                checker4 = True
                                                #in this for loop, allCoursesDep values are calculated										
                                                #we look at all of the instructors for a course
                                                for x in data[course] :
                                                        checkStaff2 = True
                                                        #checker2: checks whether or not a value exists in allcoursesdep
                                                        if checker2 == True  :
                                                                checker2 = False
                                                                if x == 'STAFF STAFF' :
                                                                        checkStaff2 = False
                                                                        allCoursesDep[key] = [[x], checkStaff2]
                                                                else :
                                                                        allCoursesDep[key] = [[x], checkStaff2]
                                                        elif x != 'STAFF STAFF' and x not in allCoursesDep[key][0] :
                                                                allCoursesDep[key][0].append(x)
                                                        if course not in allCoursesDep :
                                                                checkStaff3 = True
                                                                checker4 = False
                                                                if x == 'STAFF STAFF' :
                                                                        checkStaff3 = False
                                                                        allCoursesDep[course] = [1, [x], checkStaff3]
                                                                else :
                                                                        allCoursesDep[course] = [1, [x], checkStaff3]
                                                        else :
                                                                if checker4 == True:
                                                                        checker4 = False
                                                                        allCoursesDep[course][0] += 1
                                                                if x != 'STAFF STAFF' and x not in allCoursesDep[course][1] :
                                                                        allCoursesDep[course][1].append(x)

                                                if course not in allCoursesDep['Course'] :
                                                        #checks whether or not there is a value in allCoursesDep['Course']
                                                        if checker3 == True :
                                                                checker3 = False
                                                                #'Course' is a key that stores all courses
                                                                allCoursesDep['Course'] = [course]
                                                        else :
                                                                allCoursesDep['Course'].append(course)
                                                        
                                                        # if course code starts with a number smaller than 4, it is an undergrad course 
                                                        if int(courseTemp[index.start()]) <= 4 :
                                                                allCoursesDep['U'] += 1 
                                                        # if course code starts with a number larger than 4, it is an grad course 
                                                        else :
                                                                allCoursesDep['G'] += 1
                                        #stores the total U and G values for all semesters in range for the total offerings output
                                        semester_U += semesterL['U']
                                        semester_G += semesterL['G']
                                        #stores the data of a semester and U G I values
                                        semesterList[semester] = [data, semesterL]
                        #stores the semesterList in the corresponding addresses for "year" keys in yearList
                        yearList[year] = semesterList
                #stores the total number of U and G in order to find total offerings
                allCoursesDep['All'] = [semester_U, semester_G]
                #checks whether or not a course is opened in the given range
                existList = boolean(existList)
                #stores the yearList, allCoursesDep, existList values in the corresponding "dep" key values.
                courseList[dep] = [yearList, allCoursesDep, existList]
        return courseList

#creates the courseList dictionary consisting of all data we need
courseList = recursive(year1, semester1, year2, semester2, deps)

#constructs the dataframe dictionary that has the output table format
#we need to form "columns" to create the output in the required order
def constructFirst(year1, year2, semester1, semester2, semesters) :
        columns = ['Dept./Prog. (name)', 'Course Code', 'Course Name']
        dictList = {}
        checker2 = True
        checkSemester1 = False
        checkSemester2 = False
        a = 1
        for year in range(int(year1), int(year2)+1) :
                for semester in semesters :
                        if year == int(year1) and semester == semester1 :
                                checkSemester1 = True
                        if year == int(year2) and semester == semester2 :
                                checkSemester2 = True
                        if checkSemester1 == True and a < 2 :
                                year_semester = str(year) + '-' + semester
                                if checker2 == True :
                                        checker2 = False
                                        dictList = { 'Dept./Prog. (name)' : [None],
                                                        'Course Code' : [None],
                                                        'Course Name' : [None],
                                                        year_semester : [None],
                                                        'Total Offerings' : [None]
                                                        }
                                        columns.extend([year_semester])
                                else :
                                        dictList.update({year_semester : [None]})
                                        columns.extend([year_semester])
                        if checkSemester2 == True :
                                a += 1
        columns.extend(['Total Offerings'])
        return dictList, columns

dictList, columns = constructFirst(year1, year2, semester1, semester2, semesters)

def construct_table(courseList, year1, year2, semester1, semester2 ,semesters, deps, dictList):
        for dep in deps:
                #checks if the required output is written only once.
                checker = True
                #if a course did not open in the given range, do not show in dataframe
                if courseList[dep][2] == True :
                        # If there is "Staff Staff" in the instructors, decrease the length by 1
                        if courseList[dep][1]['I'][1] == False :
                                length_I = len(courseList[dep][1]['I'][0]) - 1
                        #else, keep it the same
                        else :
                                length_I = len(courseList[dep][1]['I'][0])
                        length = len(courseList[dep][1]['Course'])
                        #forms the string that will be written in the total U and G values of the departments
                        course_temp = 'U' + str(int(courseList[dep][1]['U'])) + ' ' + 'G' + str(int(courseList[dep][1]['G']))
                        #forms the string that will be written in the total_offerings part of the output table
                        total_offerings = 'U' + str(int(courseList[dep][1]['All'][0])) + ' ' + 'G' + str(int(courseList[dep][1]['All'][1])) + ' ' + 'I' + str(length_I)
                        #boolean variable that checks the starting year and semester of the range
                        checkSemester1 = False
                        #boolean variable that checks the ending year and semester of the range
                        checkSemester2 = False
                        a = 1
                        for year in range(int(year1), int(year2)+1) :
                                for semester in semesters :
                                        if year == int(year1) and semester == semester1 :
                                                #writes the department names in the required format
                                                stringCourse = dep[0] + '(' + removeAll(dep[1]) + ')'
                                                #sorts courses according to course codes 
                                                courseList[dep][1]['Course'] = sortedfunc(courseList[dep][1]['Course'], 0)
                                                fillspaces(dictList['Dept./Prog. (name)'], stringCourse, length)
                                                coursecode(dictList['Course Code'], course_temp, courseList[dep][1]['Course'], 0)
                                                coursecode(dictList['Course Name'], course_temp, courseList[dep][1]['Course'], 1)
                                                checkSemester1 = True
                                        if year == int(year2) and semester == semester2 :
                                                checkSemester2 = True
                                        if checkSemester1 == True and a < 2 : 
                                                year_semester = str(year) +'-' + semester 
                                                #if a course has opened in the given range, and did not open in some semesters, makes the U G and I values 0
                                                if year not in courseList[dep][0] or semester not in courseList[dep][0][year]:
                                                        year_temp = 'U' + str(0) + ' ' + 'G' + str(0) + ' ' + 'I' + str(0)
                                                        if checker == True :
                                                                checker = False        
                                                                fillspaces(dictList[year_semester], year_temp, length)
                                                        else : 
                                                                fillspaces(dictList[year_semester], year_temp, length)
                                                else :
                                                        #If "staff staff" is seen, decrease length
                                                        if courseList[dep][0][year][semester][1]['I'][1] == False:
                                                                year_temp = 'U' + str(int(courseList[dep][0][year][semester][1]['U'])) + ' ' + 'G' + str(int(courseList[dep][0][year][semester][1]['G'])) + ' ' + 'I' + str(len(courseList[dep][0][year][semester][1]['I'][0])-1)
                                                        #else keep the length same
                                                        else :
                                                                year_temp = 'U' + str(int(courseList[dep][0][year][semester][1]['U'])) + ' ' + 'G' + str(int(courseList[dep][0][year][semester][1]['G'])) + ' ' + 'I' + str(len(courseList[dep][0][year][semester][1]['I'][0]))
                                                        if checker == True :
                                                                checker = False        
                                                                xsign(dictList[year_semester], year_temp, courseList[dep][1]['Course'], courseList[dep][0][year][semester][0]) 
                                                        else :
                                                                xsign(dictList[year_semester], year_temp, courseList[dep][1]['Course'], courseList[dep][0][year][semester][0])
                                        #ends the function when the finishing semester is seen
                                        if checkSemester2 == True :
                                                a += 1  
                        #sorts the courseList
                        courseList[dep][1] = sortedfunc(courseList[dep][1], 1)
                        totalofferings(dictList['Total Offerings'], total_offerings, courseList[dep][1])
        return dictList

#puts space character "length" times 
def fillspaces(listTemp, stringCourse, length) :
        listTemp.append(stringCourse)
        while length != 0 :
                listTemp.append(' ')
                length = length - 1

#Creates the course code and course name columns of the output table
def coursecode(listTemp, course_temp, temp, control) :
        check = True
        for x in temp:
                if check == True:
                        #control=0 means course code
                        if control == 0:
                                listTemp.append(course_temp)
                        #control=1 means course name		
                        else :
                                listTemp.append(' ')
                check = False
                if control == 0 :
                        listTemp.append(x[0])
                else :
                        listTemp.append(x[1])

#puts the x sign in required places              
def xsign(listTemp, a, allList, semesterList) :
        listTemp.append(a)
        for x in allList :
                #if an element in allList is in semesterList, puts 'x'
		#meaning that the course is opened in that semester
                if x in semesterList :
                        listTemp.append('x')
                #else, puts ' ' 
                else :
                        listTemp.append(' ')

#finds the total offerings for U G and I
def totalofferings(listTemp, a, allList) :
        #the var "check" checks if the total offering is written before courses are written separately
        check = True
        for x in allList :
                if check == True :
                        listTemp.append(a)
                check = False
                #finds the total number of courses opened and total number of instructors 
                if x[0] != 'U' and x[0] != 'G' and x[0] != 'Course' and x[0] != 'All' and x[0] != 'I':
                        #If "staff staff" is seen, decreases the length
                        if x[1][2] == False :
                                strTemp = str(x[1][0]) + '/' + str(len(x[1][1]) - 1)
                        #else keeps the length constant	
                        else :
                                strTemp = str(x[1][0]) + '/' + str(len(x[1][1]))
                        #appends the information to the output	
                        listTemp.append(strTemp)

#function that sorts the dictionary without losing the key values
def sortedfunc(listTemp, control) :
        #if control == 0 we need to sort values
        if control == 0 :
                listTemp1 = sorted(listTemp, key = lambda kv : kv[0])
        #else we need to sort keys
        else :
                listTemp1 = []
                for x in sorted(listTemp):
                        listTemp1.append([x,listTemp[x]])
        return listTemp1 

dictAllList = construct_table(courseList, year1, year2, semester1, semester2,semesters, deps, dictList)

df = pd.DataFrame(dictAllList, columns = columns)
df = df.iloc[1:]
csvFormat = df.to_csv(encoding='utf-8', index=False)
print(csvFormat)
