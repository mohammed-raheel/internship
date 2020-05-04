#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import requests
import bs4

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  
  baseUrl = 'http://localhost:8888/view/Documents/PYTHON/babynamescopy/'
  
  requestUrl = baseUrl + filename
  year = re.findall('^\D+(\d{4,4})\.\D',filename)
  #print(year)
  
  s = requests.Session()
  
  resp = s.get(requestUrl,headers={'Authorization': 'token 2b0795819f358bcb65b7ad957e334f913530604b047d7f45'})
  print('Learn code response status: ',resp.status_code)

  soup = bs4.BeautifulSoup(resp.text, 'lxml')
  #print(resp.content)

  x = soup.select('iframe')
  if len(x)==0:
    print('Please check the token in the python script. Assign it a value of token of jupyter on your machine')
    return
  
  link2 = 'http://localhost:8888/' + x[0]['src'][1:]
  #print(link2)
  resp2 = s.get(link2,headers={'Authorization': 'token 2b0795819f358bcb65b7ad957e334f913530604b047d7f45'})
  
  soup2 = bs4.BeautifulSoup(resp2.text,'lxml')
  table = soup2.find('table',summary="Popularity for top 1000")
  #print(table)  
    
  tabRows = table.find_all('tr',{'align':'right'})
  
  lstNameRank = []
  for i in tabRows:
      #print(str(i))
      vals = re.findall(r'<td>(\w+)</td><td>(\w+)</td><td>(\w+)</td>',str(i))
      lstNameRank.extend(vals)
        
  baby_name = dict()
  
  counter = 0
  duplicateName = []
  for i in lstNameRank:
      rank = i[0]
      boyName = i[1]
      girlName = i[2]
      
      # Check if the boyname already exists
      if boyName in baby_name and int(baby_name[boyName]) < int(rank):
          duplicateName.append(boyName)
      else:
          baby_name[boyName] = rank
      
      if girlName in baby_name and int(baby_name[girlName]) < int(rank):
          duplicateName.append(girlName)
      else:
          baby_name[girlName] = rank
      
      counter+=1
  
  sortedVals = dict()
  for i in sorted(baby_name.keys()):
    sortedVals[i] = baby_name[i]
    
  finalResult = []
  finalResult.append(year[0])
  for i in sortedVals:
    finalResult.append(i + ' ' + sortedVals[i])
    
  #print(finalResult)
  f = open('finalNameRank.txt','a+')
  f.write('\n'.join(finalResult))
  f.write('\n')
  f.close()
  print('Output written to finalNameRank.txt file')
  return 


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.

  args = sys.argv[1:]

  if not args:
    print('usage: [--summaryfile] file [file ...]')
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  for i in args:
      #print(i)
      extract_names(i)
  
if __name__ == '__main__':
  main()
