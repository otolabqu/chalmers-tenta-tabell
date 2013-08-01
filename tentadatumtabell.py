# -*- coding: utf-8 -*-

from input import *
from output import *
import datetime
from prgdicts import BSCdict, MSCdict

def main():
    datatabell = {}
    parser = MyHTMLParser()
    parser.courseCode = None
    parser.findCourseName = False
    parser.tabell = datatabell

#    datatabell är en dict som tar en coursecode som key och get en courseEntry som value #130731

    prgdict = BSCdict()
    for grade in ['1', '2', '3']:
        #requestAndWriteFile(prgdict, grade, parser)
        #requestAndParse (prgdict,grade, parser)
        readFileAndParse(prgdict,grade,parser)

    prgdict = MSCdict()
    for grade in ['1', '2']:
        #requestAndWriteFile(prgdict,grade,parser)
        #requestAndParse (prgdict, grade, parser)
        readFileAndParse (prgdict, grade, parser)

    #debug check, manual check finds no doubles in indata key
    utdatatabell = []

    #doubles must have been created from indata -> utdata.
    #indeed the indata table has 3x each date entry...
    print (datatabell["TDA550"])

    #makeUtdataFromIndata(datatabell, utdatatabell)

    #printAsCSV (utdatatabell)  #For use with Tableau

if __name__ == '__main__':
    main()

# Todo: Add the V or H letter to indicate the location
# Todo: Add ical or gcal output
# Todo: Handle "Ges av inst"
# Todo: Add to each tentainstans a tag specifying which programme it is part of. Then make a searchable database for all programmes
# Todo: (130721) make a figure/schema of the internal data strucutre used, for better abililty to develop further
# Todo: (130727) make parallell HTTP requests to speed up that bottleneck

#130727 adjustment for Tableau: We rather create lots of doubles to be able to match every program that has a course,
# and then filter them out with Tableau. That way we don't miss courses because we filter them wrong.
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

