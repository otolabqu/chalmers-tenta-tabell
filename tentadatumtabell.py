# -*- coding: utf-8 -*-

from input import *
from output import *
import datetime
from prgdicts import BSCdict, MSCdict


def loopthrough(func):  #func is either "request" or parser, with different purposes
    prgdict = BSCdict()
    for grade in ['1', '2', '3']:
        if func =="request":
            requestAndWriteFile(prgdict, grade)
        else:
            readFileAndParse(prgdict,grade,func)

    prgdict = MSCdict()
    for grade in ['1', '2']:
        if func =="request":
            requestAndWriteFile(prgdict,grade)
        else:
            readFileAndParse (prgdict, grade, func)



def main():

    if(False):
        loopthrough ("request")

    if (True):
        parser = MyHTMLParser()
        parser.courseCode = None
        parser.findCourseName = False
        parser.tabell = {}
        loopthrough (parser)
        utdatatabell = []
        makeUtdataFromIndata(parser.tabell, utdatatabell)
        printAsCSV (utdatatabell)  #For use with Tableau

#    datatabell är en dict som tar en coursecode som key och get en courseEntry som value #130731




if __name__ == '__main__':
    main()

# Todo: Add the V or H letter to indicate the location
# Todo: Add ical or gcal output  http://productforums.google.com/forum/#!topic/calendar/Ovj6BNTQNL0   should be usable with URL actions
#          http://tardate.com/tools/kalinka.htm
# Todo: Handle "Ges av inst"  i input.py
# Todo: Add to each tentainstans a tag specifying which programme it is part of. Then make a searchable database for all programmes
# Todo: (130721) make a figure/schema of the internal data strucutre used, for better abililty to develop further
# Todo: (130727) make concurrent HTTP requests to speed up that bottleneck
# Todo: (130802) Add post-processing to fix the åäöÅÄÖ problem
# Todo: (130820) Make automatic get all the new program URLS from the search form on  https://www.student.chalmers.se/sp/program_list
#130727 adjustment for Tableau: We rather create lots of doubles to be able to match every program that has a course,
# and then filter them out with Tableau. That way we don't miss courses because we filter them wrong.
#130802 : the course codes for BSc projects don't match the pattern since they have a AAAX00 pattern. adds support for that.

#130806 Todo: Add the following programmes
##https://www.student.chalmers.se/sp/programplan?program_id=1041
##https://www.student.chalmers.se/sp/programplan?program_id=1036
##https://www.student.chalmers.se/sp/programplan?program_id=1022
##https://www.student.chalmers.se/sp/programplan?program_id=1037
##https://www.student.chalmers.se/sp/programplan?program_id=1057&grade=1&conc_id=-1
##https://www.student.chalmers.se/sp/programplan?program_id=1038&grade=1&conc_id=-1
##https://www.student.chalmers.se/sp/programplan?program_id=1021
##https://www.student.chalmers.se/sp/programplan?program_id=1039
##https://www.student.chalmers.se/sp/programplan?program_id=1040&grade=3&conc_id=-1
##https://www.student.chalmers.se/sp/programplan?program_id=1043
##https://www.student.chalmers.se/sp/programplan?program_id=1042
##https://www.student.chalmers.se/sp/programplan?program_id=1044
##https://www.student.chalmers.se/sp/programplan?program_id=1020
##https://www.student.chalmers.se/sp/programplan?program_id=1055
##https://www.student.chalmers.se/sp/programplan?program_id=1056
##https://www.student.chalmers.se/sp/programplan?program_id=1059
##https://www.student.chalmers.se/sp/programplan?program_id=1045
##

#-------------------------------------------------------------------------------
# Name: module2
# Purpose:
# Get exam dates from Chalmers Studieportalen and output them in a more readable and planning-friendly form,
# in chronological order and all 3 years of the BSc program on one page.
# Plan your exam periods and re-exams easier with this tool.
# Tested on the TKDAT-pages but should work with any URL from studieportalen BSc programme.
#
# En kurskod kommer alltid först. När vi läst in en kurskod kan vi läsa in en href som säger att här kommer kursnamnet.
# Sen kollar vi efter datumsträngar och lägger till dem i en dict med den aktuella kursen.
# Sen sparar vi allt och outputar fint

# Hitta en kurskod och spara som AKTUELL kurskod i parsern.
# Samtidigt skapas ett nytt entry i dicten om det inte redan finns, för denna kurs
# Sedan extraheras kursens namn ur parsern
# Samt upp till 3 datum
# Sedan kommer nästa kurs, och repeat

# Author: natwei
#
# Created: 06/04/2013
# Copyright: (c) natwei 2013
# Licence: <your licence>
# Using python 3.3 with
# http://docs.python-requests.org/en/latest/
# http://docs.python.org/2/library/htmlparser.html
# to run this type in the console for example
# python tentadatumtabell.py > tabell.html
#-------------------------------------------------------------------------------

