# -*- coding: utf-8 -*-
import requests
#from html.parser import HTMLParser  #python 3
from HTMLParser import HTMLParser    #python 2.7



def requestProgramList (): #130731 added another middle step to waste less time
        url = 'https://www.student.chalmers.se/sp/program_list?flag=1&query_start=1&batch_size=200&sortorder=NAME&search_ac_year=2014/2015'
        print (url)
        data = requests.get (url).text
        data = data.encode ('utf-8')
        print ("got program list")
        return data

class MyHTMLParserForProgramList(HTMLParser):
        #def __init__(self):
         #   super.__init__(super)
          #  self.courseCode = None

        def handle_starttag(self, tag, attrs):
            print ("starttag ,", tag)


        def handle_endtag(self, tag):
            print ("endtag ,", tag)

        def handle_data(self, data):
            print ("data")

def main():
    data = requestProgramList()
    p = MyHTMLParserForProgramList ()
    p.feed(data)


if __name__ == '__main__':
    main()
