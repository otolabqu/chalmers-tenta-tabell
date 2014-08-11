# -*- coding: utf-8 -*-

#created 2014-08-10
#file for getting all the program acronyms and other info
#which can then be used in the other parts of this program

#see bottom for excerpt from website that this is coded for

#example terminal command to run :
# python programlist.py > programlistlog
# will give you the log in the file "programlistlog"  and the CSV output in the file "programlist.txt"

import requests
#from html.parser import HTMLParser  #python 3
from HTMLParser import HTMLParser    #python 2.7


#States
READY_TO_ADD = 1
FIND_NEW_CODE = 11
ADDING_NEW   = 12
GET_ACRONYM  = 13

READY_TO_GET_LONG_NAME = 14
GET_LONG_NAME = 15
READY_TO_GET_HP =16
GET_HP = 17

FINISHED = 20

outerDict = {}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def requestProgramList ():
        url = 'https://www.student.chalmers.se/sp/program_list?flag=1&query_start=1&batch_size=200&sortorder=NAME&search_ac_year=2014/2015'
        print (url)
        data = requests.get (url).text
        data = data.encode ('utf-8')
        print ("got program list")
        return data

class MyHTMLParserForProgramList(HTMLParser):


        def handle_starttag(self, tag, attrs):
            if tag == "tr" and  self.state == READY_TO_ADD:
                print ("state is ready to add, and found new <tr> tag. state changed to FIND_NEW_CODE")
                self.state = FIND_NEW_CODE
            if tag == "a" and self.state == FIND_NEW_CODE:
                print ("state is FIND_NEW_CODE, and found <a>. State changes to ADDING_NEW")
                self.state = ADDING_NEW

                for (k,v) in attrs:
                    if k == 'href':
                        programId = v.split ('=') [1] # "programplan?program_id=1214"
                        print (programId)
                        self.substate = programId
                        outerDict [programId] = {}  #creates new entry

                self.state = GET_ACRONYM
                print ("changing state to GET_ACRONYM")
            if self.state == READY_TO_GET_LONG_NAME and tag == "a":
                self.state = GET_LONG_NAME
            if self.state == READY_TO_GET_HP and tag == "small":
                self.state = GET_HP



        def handle_endtag(self, tag):
            if self.state != 0 and tag == 'table':
                self.state = FINISHED
                print ("changed state to FINISHED (found </table> ) ")


        def handle_data(self, data):
            if "Högskolepoäng" in data: #hardcoded to initiate actual reading of data
                self.state = READY_TO_ADD
            if self.state == GET_ACRONYM:
                outerDict [self.substate] ['acronym'] = data
                print ("saved acronym" , data, " in outerdict entry for " , self.substate )
                self.state = READY_TO_GET_LONG_NAME
                print ("changed state to READY_TO_GET_LONG_NAME")
            if self.state == GET_LONG_NAME:
                outerDict [self.substate] ['long_name'] = data
                print ("saved long name" , data, " in outerdict entry for " , self.substate )
                self.state = READY_TO_GET_HP
                print ("changed state to READY_TO_GET_HP")
            if self.state == GET_HP:
                data = data.replace (',' , '.') #to fit the number format
                if is_number(data):
                    pass
                else:
                    data = "NA"

                outerDict [self.substate] ['hp'] = data
                print ("saved hp" , data, " in outerdict entry for " , self.substate )
                print ("entry finished " , self.substate)
                print ("changing substate to 0 and state to READY_TO_ADD")
                self.substate = 0
                self.state = READY_TO_ADD
                print ("changed state to READY_TO_ADD")



def main():
    data = requestProgramList()
    p = MyHTMLParserForProgramList ()
    p.state = 0
    p.substate = 0
    p.feed(data)

    filename = "programlist.txt"
    f = open(filename, 'w')
    f.write ("id ; acronym ; longname ; hp \n")

    for k in outerDict.keys():
        s = ""
        s = s + k + " ; "
        v = outerDict[k]
        for k1 in v:
            s = s + str( v[k1]) + " ;"
        s = s[:-1] +  "\n"  #remove last ; and add newline
        f.write (s)
    f.close()
    print ("wrote data to file " , filename)
    return outerDict

def getProgramDict ():
    return main()

if __name__ == '__main__':
    main()

# HTML sample from
# https://www.student.chalmers.se/sp/program_list?flag=1&query_start=1&batch_size=200&sortorder=NAME&search_ac_year=2014/2015
#
# <td colspan="3"><a href="https://www.student.chalmers.se/sp/program_list?flag=1&sortorder=CREDIT_SORT,CODE&search_ac_year=2014/2015" class="tableHeaderLink">Högskolepoäng</a></td>
# 	</tr>
#
#   	<tr>
# 		<td valign="top"><small><b><a href="programplan?program_id=1214">TAFFK</a></b></small></td>
#                 <td valign="top"><small><b><a href="programplan?program_id=1214">AFFÄRSUTVECKLING OCH ENTREPRENÖRSKAP INOM BYGGTEKNIK</a></b></small></td>
# 		<td valign="top"><small>180,0</small></td>
#                 <td><a href="programplan?program_id=1214"><img src="images/ico_info.gif" title="Programplan" border="0"></a></td>
# 		<td style="text-decoration: none">
# 			&nbsp;		</td>
# 	</tr>
#   	<tr class="fade">
# 		<td valign="top"><small><b><a href="programplan?program_id=1171">MPAME</a></b></small></td>
#                 <td valign="top"><small><b><a href="programplan?program_id=1171">APPLIED MECHANICS, MSC PROGR</a></b></small></td>
# 		<td valign="top"><small>120,0</small></td>
#                 <td><a href="programplan?program_id=1171"><img src="images/ico_info.gif" title="Programplan" border="0"></a></td>
# 		<td style="text-decoration: none">
# 			&nbsp;		</td>
# 	</tr>