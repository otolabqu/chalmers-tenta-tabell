# -*- coding: utf-8 -*-
# Todo:  Add the V or H letter to indicate the location
# Todo:  Add ical or gcal output
# Todo:  Handle "Ges av inst"
# Todo:  Make a version compatible with MSc programmes (only 2 years , any other difference?)
# Todo:  Make the whole process automated for all the BSc and MSc programmes in Chalmers and output a complete webpage with all of those. Then publish it.
# Todo:  Add to each tentainstans a tag specifying which programme it is part of. Then make a searchable database for all programmes

#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#   Get exam dates from Chalmers Studieportalen and output them in a more readable and planning-friendly form,
#   in chronological order and all 3 years of the BSc program on one page.
#   Plan your exam periods and re-exams easier with this tool.
#   Tested on the TKDAT-pages but should work with any URL from studieportalen BSc programme.
#
#
#
#
#
#   En kurskod kommer alltid fÃƒÆ’Ã‚Â¶rst. NÃƒÆ’Ã‚Â¤r vi lÃƒÆ’Ã‚Â¤st in en kurskod kan vi lÃƒÆ’Ã‚Â¤sa in en href som sÃƒÆ’Ã‚Â¤ger att hÃƒÆ’Ã‚Â¤r kommer kursnamnet.
#   Sen kollar vi efter datumstrÃƒÆ’Ã‚Â¤ngar och lÃƒÆ’Ã‚Â¤gger till dem i en dict med den aktuella kursen.
#   Sen sparar vi allt och outputar fint

#   Hitta en kurskod och spara som AKTUELL kurskod i parsern.
#   Samtidigt skapas ett nytt entry i dicten om det inte redan finns, fÃƒÆ’Ã‚Â¶r denna kurs
#   Sedan extraheras kursens namn ur parsern
#   Samt upp till 3 datum
#   Sedan kommer nÃƒÆ’Ã‚Â¤sta kurs, och repeat

#   NÃƒÆ’Ã‚Â¤r alla kurser ÃƒÆ’Ã‚Â¤r inlÃƒÆ’Ã‚Â¤sta i en bra tabell kan vi outputta dem i en annan form. Det lÃƒÆ’Ã‚Â¶ser vi sen.


# Author:      natwei
#
# Created:     06/04/2013
# Copyright:   (c) natwei 2013
# Licence:     <your licence>
# Using python 3.x  with
# http://docs.python-requests.org/en/latest/
# http://docs.python.org/2/library/htmlparser.html
# to run this type in the console for example
# python tentadatumtabell.py > tabell.html
#-------------------------------------------------------------------------------
import requests
from html.parser import HTMLParser
import datetime

#Efter att ha lÃƒÆ’Ã‚Â¤st in alla datum konverteras till detta format som ÃƒÆ’Ã‚Â¤r lÃƒÆ’Ã‚Â¤mpligt fÃƒÆ’Ã‚Â¶r output
class TentaInstans():
    def __init__(self):
        self.date = None
        self.courseCode = None
        self.courseName = None
    def __repr__(self):  #formatting for text output
        return self.readableDate() +" " + self.fmem() + " " + self.courseCode+ " "+ self.courseName + " "

    def html (self, addDate):
        basestring = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
        datestring = self.readableDate() if addDate else ""
        return basestring.format(datestring, self.fmem(), self.courseCode, self.courseName)

    def keyfunction (i1):  #key function for list sorting
        return i1.date
    def readableDate (self):
        return self.date[0:4]+'-'+self.date[4:6]+'-'+self.date[6:8]#+' ' + self.fmem() + ' ' + self.date[10:]

    def fmem(self): #corrects the previously introduced error of "em" -> "kv"
        if self.date[8:10] == "kv":
            return "em"
        return "fm"


#AnvÃƒÆ’Ã‚Â¤nds vid inlÃƒÆ’Ã‚Â¤sning
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

    def __repr__(self):
        s = self.name + " " + self.code + " "
        for t in self.datumlista:
            s = s + t.__repr__()
        return s


class MyHTMLParser(HTMLParser):
        def isDate (self,text):
            #format  '11/03-2013 em M'
            text = text.lstrip().rstrip()   #remove trailing whitespaces
            if len(text) == 15:
                #print ("found 15 character data: ", text)
                day = text[0:2]
                month = text[3:5]
                year  = text[6:10]
                time  = text[11:13]
                if day.isdigit() and month.isdigit() and year.isdigit() and time.isalpha():
                    #print ("   found date ", text)
                    t = Tentadatum()
                    t.year = year
                    t.month = month
                    t.time= time
                    t.day = day
                    return t
                return None  #not a valid date
            return None  #not a 15 length string


        def isCourseCode ( self, text):
            #format 'DAT043'
            if len(text) == 6:
                chars = text[0:3]
                nums  = text[3:6]
                if chars.isalpha() and nums.isdigit():
                    return True

        def handle_starttag(self, tag, attrs):
           # print ("Encountered a start tag:", tag)
            if tag == 'a':
                #print (attrs)
                for (k,v) in attrs:
                    if  k == 'href':
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
            if self.findCourseName: #registrera namnet och stÃƒÆ’Ã‚Â¤ng sedan av denna sÃƒÆ’Ã‚Â¶kfunktion
                        self.tabell[self.courseCode].name = data
                        self.findCourseName = False
            t = self.isDate (data)
            if t is not None:
                self.tabell [self.courseCode].datumlista.append(t)

def main():

    datatabell = {}

    parser = MyHTMLParser()
    parser.courseCode = None
    parser.findCourseName = False
    parser.tabell = datatabell

    #TO CREATE AN URL FOR PARSING:
    #Get the URl from STUDIEPORTALEN for the BSc Programme year 1. Remove the grade number and split the string into two as follows:

    #These URL's are examples, valid for the 2012/2013 year
    stringparts = ['https://www.student.chalmers.se/sp/programplan?program_id=871&grade=','&conc_id=-1']   #TKDAT
    #stringparts = ['https://www.student.chalmers.se/sp/programplan?program_id=875&grade=','&conc_id=-1']    #TKITE
    #stringparts = ['https://www.student.chalmers.se/sp/programplan?program_id=904&grade=','&conc_id=-1']    #TKTEM
    #stringparts = ['https://www.student.chalmers.se/sp/programplan?program_id=870&grade=','&conc_id=-1']   #TKBIO

    for grade in ['1', '2', '3']:
        url = grade.join (stringparts)
        data = requests.get (url).text
        parser.feed(data)

    utdatatabell = []
    for k,v in datatabell.items():
        for d in v.datumlista:
            if d.time == "em":
                d.time = "kv"  #em kallas istÃƒÆ’Ã‚Â¤llet kvÃƒÆ’Ã‚Â¤ll, eftersom kv kommer efter fm, sÃƒÆ’Ã‚Â¥ om tvÃƒÆ’Ã‚Â¥ tentor har samma datum kan string compare sortera dem rÃƒÆ’Ã‚Â¤tt enligt "fm" "em"
            i = TentaInstans()
            i.date = d.year+d.month+d.day+d.time
            i.courseCode = v.code
            i.courseName = v.name
            utdatatabell.append(i)


    sorterad = sorted (utdatatabell, key = TentaInstans.keyfunction )

    now = datetime.datetime.now()
    now = str(now).replace('-', '')
    #print (now)

    lastdate = "" #used for not printing dates more than necessary in table. Increases readability.
    print ('<table border="1">')
    print ("<th> Datum </th>")
    print ("<th> </th>")
    print ("<th> Kurskod </th>")
    print ("<th> Namn </th>")
    for x in sorterad:
       # print (x.date[0:-2])
        if x.date > now: #we want to print it
            currentDateWithoutFMEM = x.date[0:-2]
            if currentDateWithoutFMEM > lastdate: #print full with date
                print(x.html(True))
                lastdate = currentDateWithoutFMEM
            else:
                print(x.html(False))

    print ("</table>")
if __name__ == '__main__':
    main()
