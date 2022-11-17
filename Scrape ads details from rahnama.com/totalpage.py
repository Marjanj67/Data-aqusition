
import re
import requests
from bs4 import BeautifulSoup

# global variables read phone number
curUrl = 0
phoneNum = 0
title = 0
allData = {'a':'123'}


# global variables for total urls
cpageUrl = 0
allurls = []
finalUrls = []

def mylinks(href):
  global allurls
  if href != None and href != "":
    ch = '/item' in str(href)
    if ch == True:
      allurls.append(href)
      return href

def mylinks2(next):
  global allurls
  slinks =re.findall(r'[:][\d]{6}',str(next))
  for m in slinks:
    m = m.replace(":","/item/")
    allurls.append(m)


def main():
  global cpageUrl,allurls
  # ------- getting urls
  u = open ("BaseUrls.txt", "r")
  for i in u:
    cpageUrl = i.removesuffix('\n')
    weburl = requests.get(cpageUrl).text
    soup = BeautifulSoup(weburl,'html.parser')
    s1 = soup.find_all(href=mylinks)
    s4 = soup.find_all(id= "__NEXT_DATA__")
    mylinks2(s4)

  # ------- reading old urls
  u1 = open("oldUrls.txt","r")
  oldUrls = set('0')
  for i in u1:
    if i != 0:
      i = i.removesuffix('\n')
      oldUrls.add(i)

 # ------- writing urls in a file
  f=open("newUrl.txt","w+")
  allurls2 = set(allurls)
  for x in allurls2:
    ch = x in oldUrls
    if x != 0 and  ch == False:
      finalUrls.append(x)
      f.write(x+ "\r")

  # ------- getting details-------------------------------------------------------
  index = 0 
  for i in finalUrls:
    if i!=0:
      curUrl = "https://rahnama.com" + i.removesuffix('\n')
      co = requests.get(curUrl).status_code
      if  co== 200:
        try:
          webUrl = requests.get(curUrl).text
          soup1 = BeautifulSoup(webUrl,'html.parser')
          p1 = soup1.find_all(attrs={"name": "description"})
          # print(p1[0])
          phoneNum = re.findall(r"[0][\d]{10}|[9][\d]{9}|[\+98][\d]{12}",str(p1[0]))
          title = soup1.select('title')[0].text
          allData[title]= phoneNum
        except:
          print("Something went wrong")

        index = index + 1
      else:
        index = index + 1
    
  # open data file
  m = open("newNums.txt", "w", encoding="utf-8")
  # read old numbers
  u = open("oldNums.txt", "r", encoding="utf-8")
  oldNumbers = []
  for i in u:
    if i != 0:
      i = i.removesuffix('\n')
      oldNumbers.append(i)

  # compare and add new numbers 
  newNumbers = []
  for key,value in allData.items():
    if value != "" and value != []:
      newNumbers.append(value[0])

  uniqueNum = set(newNumbers) - set(oldNumbers)
  for j in uniqueNum:  
    if j.startswith("09") or j.startswith("+989")or j.startswith("9"):
      value1 = (j)
      m.write(value1 + "\r")

if __name__ == "__main__":
  main();
  