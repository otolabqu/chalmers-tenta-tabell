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



#AnvÃ¤nds vid inlÃ¤sning
class Tentadatum ():
    def __init__(self):
        self.year = None
        self.month = None
        self.day = None
        self.time = None

    def __repr__(self):
        return self.year + " " + self.month + " " + self.day + " " + self.time

    def __eq__ (self, other):  #this solved the list check problem with tentadatum in list, which was not done correctly before
        if isinstance(other, self.__class__):
            if self.year == other.year and self.month== other.month and self.day == other.day and self.time == other.time:
                return True
        return False

    def __ne__ (self,other):
        return not self.__eq__ (other)

class CourseEntry ():
    def __init__(self):
        self.name = ""
        self.code = ""
        self.datumlista = []
        self.progYear= [] #added 130731 to replace year % programme, for better Tableau funcitonality
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
                        if not data in self.tabell: #130731 The same course code & tentadatum may appear in multiple programmes & years. They all share one entry in the indata-table
                            self.tabell[data] = CourseEntry ()
                            self.tabell[data].code = data
                        #make them hashable and use dict instead. will be nicer 130801

                        gp = (self.grade, self.progr)
                        py = self.tabell[data].progYear
                        if not gp in py:  #this solves the problem of making doubles when a course appears twice in the same prog, year. but code is ugly
                            py.append (gp)
                        #self.tabell[data].progYear.append( (self.grade, self.progr)) #130731 adds the tuple of progYear, for better Tableau functionality. Shall replace grade, prog below
                        #if self.courseCode== "TIN092":
                         #   print (py)
            if self.findCourseName: #registrera namnet och stÃ¤ng sedan av denna sÃ¶kfunktion
                        self.tabell[self.courseCode].name = data
                        self.findCourseName = False
            t = self.isDate (data)
            if t is not None:
                dl = self.tabell [self.courseCode].datumlista
                if not t in dl: #fix to not create lots of doubles
                    dl.append(t)

def requestAndWriteFile (prgdict, grade, parser): #130731 added another middle step to waste less time
     for p in prgdict:
        filename = p + "-" + grade + ".txt"
        f = open(filename, 'w')
        url = 'https://www.student.chalmers.se/sp/programplan?program_id={}&grade={}&conc_id=-1'.format (prgdict[p], str(grade))
        data = requests.get (url).text
        f.write (data)
        f.close()

def readFileAndParse(prgdict, grade, parser):
    for p in prgdict:
        filename = p + "-" + grade + ".txt"
        f = open(filename, 'r')
        data = f.read()

        outgrade = int(grade)

         #WHY does the below reduce the data by 75% ???
        if p[0:2] == "MP" and outgrade < 3: #offset the year for MSc programmes for more usefulness
            outgrade += 3
        #    grade += 3
        parser.grade = outgrade #added 130721 for Tableau. Not the best way to do it, but will work
        parser.progr = p     #added 130721, same as above
        parser.feed(data)


#deprecated 130801 may not work properly
def requestAndParse(prgdict, grade, parser): #to make it work you need to re-activate the ## lines below
    for p in prgdict:
        #print (p)
        url = 'https://www.student.chalmers.se/sp/programplan?program_id={}&grade={}&conc_id=-1'.format (prgdict[p], str(grade))
        data = requests.get (url).text

        grade = int (grade)

        #print ("NEW PAGE")
        #print (p, grade)
        #print (data)
         #WHY does the below reduce the data by 75% ???
       # if p[0:2] == "MP" and grade < 3: #offset the year for MSc programmes for more usefulness
        #    grade += 3   #in this case
        parser.grade = grade #added 130721 for Tableau. Not the best way to do it, but will work
        parser.progr = p     #added 130721, same as above
        parser.feed(data)