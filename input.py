#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      natwei
#
# Created:     27-07-2013
# Copyright:   (c) natwei 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import requests
from html.parser import HTMLParser



#Används vid inläsning
class Tentadatum ():
    def __init__(self):
        self.year = None
        self.month = None
        self.day = None
        self.time = None

    def __repr__(self):
        return self.year + " " + self.month + " " + self.day + " " + self.time


class CourseEntry ():
    def __init__(self):
        self.name = ""
        self.code = ""
        self.datumlista = []
        self.year = 0 #added 130721 for more functionality
        self.programme = "" #added 130721 for more functionality

    def __repr__(self):
        s = self.name + " " + self.code + " "
        for t in self.datumlista:
            s = s + t.__repr__()
        return s



class MyHTMLParser(HTMLParser):
        #def __init__(self):
         #   super.__init__(super)
          #  self.courseCode = None
           # self.findCourseName = False


        def isDate (self,text):
            #format '11/03-2013 em M'
            text = text.lstrip().rstrip() #remove trailing whitespaces
            if len(text) == 15:
                #print ("found 15 character data: ", text)
                day = text[0:2]
                month = text[3:5]
                year = text[6:10]
                time = text[11:13]
                if day.isdigit() and month.isdigit() and year.isdigit() and time.isalpha():
                    #print (" found date ", text)
                    t = Tentadatum()
                    t.year = year
                    t.month = month
                    t.time= time
                    t.day = day
                    return t
                return None #not a valid date
            return None #not a 15 length string


        def isCourseCode ( self, text):
            #format 'DAT043'
            if len(text) == 6:
                chars = text[0:3]
                nums = text[3:6]
                if chars.isalpha() and nums.isdigit():
                    return True

        def handle_starttag(self, tag, attrs):
           # print ("Encountered a start tag:", tag)
            if tag == 'a':
                #print (attrs)
                for (k,v) in attrs:
                    if k == 'href':
                        if 'course?course_id=' in v:
                            #print (k, " " , v)
                            self.findCourseName = True

        def handle_endtag(self, tag):
            pass #print ("Encountered an end tag :", tag)
        def handle_data(self, data):
            if self.isCourseCode (data):
                if self.courseCode != data:
                        #print ("found new course code: ", data)
                        self.courseCode = data
                        self.tabell[data] = CourseEntry ()
                        self.tabell[data].code = data
                        self.tabell[data].grade = self.grade #added 130721
                        self.tabell[data].progr = self.progr #added 130721

            if self.findCourseName: #registrera namnet och stäng sedan av denna sökfunktion
                        self.tabell[self.courseCode].name = data
                        self.findCourseName = False
            t = self.isDate (data)
            if t is not None:
                self.tabell [self.courseCode].datumlista.append(t)


def requestAndParse(prgdict, grade, parser):
    for p in prgdict:
        url = 'https://www.student.chalmers.se/sp/programplan?program_id={}&grade={}&conc_id=-1'.format (prgdict[p], grade)
        data = requests.get (url).text
        parser.grade = grade #added 130721 for Tableau. Not the best way to do it, but will work
        parser.progr = p     #added 130721, same as above
        parser.feed(data)