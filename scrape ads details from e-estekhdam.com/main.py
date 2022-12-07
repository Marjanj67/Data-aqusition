from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
import re
from soupsieve import escape


# today date -------
Today = "2022-12-07"
# today date -------



def linkDate(Soup):
  DateTag = Soup.find_all("time")[0]
  AdDate = 0
  DateTag1 = DateTag['datetime'].split('T')
  AdDate = DateTag1[0]
  return AdDate

def find_number(Soup):
  phoneNum = 0
  Nums = Soup.find_all('a',{'href':re.compile('^tel:.*')})
  for n in Nums:
    if phoneNum ==0:
      NumsSplit = str(n).split('tel:')[1]
      NumsSplit = str(NumsSplit).split('"')[0]
      if NumsSplit.startswith('09') or NumsSplit.startswith('+989'):
        phoneNum = NumsSplit
  return phoneNum

def get_urls():
  AllUrls=[]
  u = open ("BaseUrls.txt", "r")
  old = open("oldUrls.txt","r", encoding="utf-8")

  for i in u:
    CurrentUrl = i.removesuffix('\n')
    try:
      weburl = requests.get(CurrentUrl).text
      soup = BeautifulSoup(weburl,'html.parser')
      Links = soup.find_all('a',{'href':re.compile(r'^(\/k).*')})
    except:
      print("there is an error")
    for li in Links:
      SplitUrl = str(li).split('"')
      url = [x for x in SplitUrl if x.startswith('/k')][0]
      url = 'https://www.e-estekhdam.com' + str(url)
      Repeat = 0
      for k in old:
        if k.removesuffix('\n') == str(url):
          Repeat = 1
      if Repeat == 0:
        AllUrls.append(url)
  return AllUrls

def write_in_file(FileName,NewUrls):
  string = str(FileName) + '.txt'
  f=open(string,"w+", encoding="utf-8")
  for x in NewUrls:
    if x != 0:
      f.write(x+ "\r")

def get_details(CurrentUrl):
  Detail = []
  try:
    co = requests.get(CurrentUrl).status_code
  except:
    print("error")
    co = 100
  if co == 200:
    weburl = requests.get(CurrentUrl).text
    soup1 = BeautifulSoup(weburl,'html.parser')
    AdDate = linkDate(soup1)
    PhoneNum = find_number(soup1)
    title = soup1.select('title')[0].text
    if AdDate == Today:
      Detail = str(title) + ',' + str(PhoneNum)
  return Detail


def main():
  NewUrls = get_urls()
  FileName = 'newUrl'
  write_in_file(FileName,NewUrls) # ------- writing urls in a file
  Details = []
  for CurrentUrl in NewUrls: 
    Detail = get_details(CurrentUrl) # ------- getting details------------
    Details.append(Detail)
  FileName = 'newData'
  write_in_file(FileName,Details)




if __name__ == "__main__":
  main();
  
