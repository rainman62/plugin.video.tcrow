import re

data = ''
with open ("hello.txt", "r") as myfile:
    data=myfile.read()

inputHTML = str(data)
inputHTML = inputHTML[inputHTML.find('<main'):]
returnValue = {}
# returnValue.append({'link': link, 'title': title, 'image': image})
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print tag," " , attrs
        if tag=='a': # and len(attrs)==2 and attrs[0][0]=='href' and attrs[1][0]=='title':
            print tag
# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed(inputHTML)

print returnValue