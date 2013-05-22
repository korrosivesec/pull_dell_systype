import re
import sys
import os
import string
from urllib2 import URLError, urlopen, Request

#Given a list of tags, this pulls the model number from support.dell.com
#Inspired from code found at http://ninet.org/2010/01/dell-scraper/

def processHTML(rawhtml):
  #Grab System Type
  res = re.search('<title>Product Support for\s(.+)\s\|', rawhtml, re.IGNORECASE)
  try:
    SysType = res.group(1)
    print SysType
    return SysType
  except:
    SysType = "Tag not found"
    return SysType
    
#fileI/O
def readfile(inFile):
  if os.path.isfile(inFile) == False:
    exit()
 
  thisfile = open(inFile, 'r')
 
  tags = []
  taga = tags.append
  for line in thisfile.readlines():
    if line.strip(): # check for empty lines
      if line[-1] == '\n':
        taga(line[0:-1]) # If line ends in line break remove it
      else:
        taga(line)
  thisfile.close()
  return tags

def writefile(outfile, outline):
  thisfile = open(outfile, 'a')
  thisfile.write(outline + "\n")
  thisfile.close()

#format data and write
def fdata(tag, SysType):
  outstr = '"' + tag + '","' + SysType + '"'
 
  return outstr

  ###  MAIN ###
 
url = 'http://www.dell.com/support/troubleshooting/us/en/04/Servicetag/'
 
filename = 'taglist.txt'
tags = readfile(filename)
 
for tag in tags:
  try:
    print 'Current request is: ' + url + tag + '%3Fs%3DBIZ'
    req = Request(url + tag + "%3Fs%3DBIZ")
    response = urlopen(req)
    rawhtml = response.read()
    SysType = processHTML(rawhtml)
    outstr = fdata(tag, SysType)
    print outstr
    writefile("./SystemList.txt", outstr)
  except URLError, e:
    if hasattr(e, 'reason'):
      print 'We failed to reach a server.'
      print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
      print 'The server couldn\'t fulfill the request.'
      print 'Error code: ', e.code