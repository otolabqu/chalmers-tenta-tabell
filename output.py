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

#Efter att ha lÃ¤st in alla datum konverteras till detta format som Ã¤r lÃ¤mpligt fÃ¶r output
class TentaInstans():
    def __init__(self):
        self.date = None
        self.courseCode = None
        self.courseName = None
        self.grade = None
        self.progr = None

    def __repr__(self): #formatting for text output
        return self.readableDate() +" " + self.fmem() + " " + self.courseCode+ " "+ self.courseName + " "

    def html (self, addDate):
        basestring = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
        datestring = self.readableDate() if addDate else ""
        return basestring.format(datestring, self.fmem(), self.courseCode, self.courseName)

    def csv (self):  #added 130721 for csv output for use with Tableau
        basestring = ' {}; {}; {}; {}; {}; {}'
        return basestring.format (self.readableDate(), self.fmem(), self.progr, self.grade, self.courseCode, self.courseName)

    def keyfunction (i1): #key function for list sorting
        return i1.date
    def readableDate (self):
        return self.date[0:4]+'-'+self.date[4:6]+'-'+self.date[6:8]#+' ' + self.fmem() + ' ' + self.date[10:]

    def fmem(self): #corrects the previously introduced error of "em" -> "kv"
        if self.date[8:10] == "kv":
            return "em"
        return "fm"






def printAsCSV (sorterad):
    #behÃ¶ver inte fixa datum, det kan tableau filtrera bort
    #behÃ¶ver inte ta bort fmem, det kan tableau anvÃ¤nda sig av
    print ("Datum; Tid; Programkod; Ã…r; Kurskod; Namn; ")  #CSV - tabellstruktur. ska sedan lÃ¤gga till fler fÃ¤lt hÃ¤r
    for x in sorterad:
        print (x.csv())

def printAsTable (sorterad):

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



def makeUtdataFromIndata (datatabell, utdatatabell):

    for k,v in datatabell.items():
        for d in v.datumlista:
            #if d.time == "em": #130731  deprecated, not needed for Tableau and we don't have backwards HTML compatability at the moment
            #    d.time = "kv" #em kallas istÃ¤llet kvÃ¤ll, eftersom kv kommer efter fm, sÃ¥ om tvÃ¥ tentor har samma datum kan string compare sortera dem rÃ¤tt enligt "fm" "em"
            for (p,y) in v.progYear:  #130731 now we want to create one list entry for each combination of coursecode, program, year
                i = TentaInstans()
                i.date = d.year+d.month+d.day+d.time
                i.courseCode = v.code
                i.courseName = v.name
                #i.grade = v.grade  # added 130721 grade is ambiguous but means year -> 1,2,3 are the possible values
                #i.progr = v.progr # added 130721...
                i.progr = p #130731
                i.grade = y #130731
                utdatatabell.append(i)
