
import re
import requests
from bs4 import BeautifulSoup


def find_links(next):
  slinks =re.findall(r'[:][\d]{6}',str(next))
  Urls = []
  for m in slinks:
    m = m.replace(":","/item/")
    m = "https://rahnama.com" + str(m)
    Urls.append(m)
  return Urls


def find_urls(oldUrls):
    u = open ("BaseUrls.txt", "r")
    AllUrls = []
    for i in u:
      cpageUrl = i.removesuffix('\n')
      weburl = requests.get(cpageUrl).text
      soup = BeautifulSoup(weburl,'html.parser')
      # s1 = soup.find_all(href=mylinks)
      LinksDala = soup.find_all(id= "__NEXT_DATA__")
      Urls = find_links(LinksDala)
      for url in Urls:
        CheckIn = url in oldUrls
        if CheckIn == False :
          AllUrls .append(url)
    return AllUrls


def read_old_urls():
  u1 = open("oldUrls.txt","r")
  oldUrls = []
  for i in u1:
    if i != 0:
      i = i.removesuffix('\n')
      oldUrls.append(i)
  return oldUrls


def write_to_file(UrlList,FileName):
  Path = str(FileName)+'.txt'
  f=open(str(Path),"w+")
  for x in UrlList:
    if x != 0 :
      f.write(x+ "\r")


def get_number_title(CurrentUrl):
  Data = ''
  PhoneNum = 0
  ## i.removesuffix('\n')
  co = requests.get(CurrentUrl).status_code
  if  co== 200:
    try:
      webUrl = requests.get(CurrentUrl).text
      soup1 = BeautifulSoup(webUrl,'html.parser')
      p1 = soup1.find_all(attrs={"class": "eHTumH"})
      # print(p1[0])
      PhoneNum = re.findall(r"[0][\d]{10}|[9][\d]{9}|[\+98][\d]{12}",str(p1[0]))
      title = soup1.select('title')[0].text
      if len(PhoneNum) >0:
        for pn in PhoneNum:
            Data= str(title) + ',' + str(pn)
    except:
      print("Something went wrong")
  return Data


def main():
  global cpageUrl,allurls
  # ------- reading old urls
  oldUrls = read_old_urls()
  # ------- getting urls
  UrlList = find_urls(oldUrls)
  UrlListUnique = set(UrlList)
  # ------- writing urls in a file
  FileName = 'newUrl'
  write_to_file(UrlListUnique,FileName)


  # ------- getting details-------------------------------------------------------
  AllDetails = []
  for CurrentUrl in UrlListUnique:
    if CurrentUrl != 0:
      TitleNumber = get_number_title(CurrentUrl)
      if TitleNumber != '':
        AllDetails.append(TitleNumber)

    
  # open data file
  m = open("newNums.txt", "w", encoding="utf-8")
  for ad in AllDetails:
    value = ad
    m.write(value + "\r")

if __name__ == "__main__":
  main();
  
