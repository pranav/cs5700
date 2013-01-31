#!/usr/bin/python

import sys
import socket
import time


from HTMLParser import HTMLParser

# Parse links from HTMLParser constructed from given html document
class LinkParser( HTMLParser ):
    def handle_starttag( self, tag, attrs ):
        if tag == 'a':
            link = next( sub1 for sub1 in attrs if 'href' in sub1 )[1]

            print link


# parse test html file
f = open( "project2.html", "r" )

html = f.read()

# Hacky and stupid way to find flags using pattern matching but easier
# than parsing
def try_to_find_flags( html ):
    html2 = html.split("<h2 class='secret_flag' style=\"color:red\">")

    if len( html2 ) > 1:
        at = html2[1]
        print at[ 0:at.find( '</h2>' ) ].strip()



# start a parser and give it html
parser = LinkParser()
parser.feed( html )

try_to_find_flags( html )

