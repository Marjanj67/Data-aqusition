from gettext import find
from pickle import UNICODE
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#global variables
keyWords = []
urlPrefix = "https://www.google.com/search?q="
relatedKeys = []   
allData = []
compLinks = []
keyPo = 0
headers = {  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'} 
def main():
    global relatedKeys, compLinks,keyPo
    # read keywords
    k = open("keyWords.txt",'r',encoding="utf-8")
    w = open("data.txt",'w',encoding="utf-8")
    for x in k:
        keyWords.append(x)
    # build url from keyword
    for i in keyWords:
        i2 = i.removesuffix("\n").split(" ")
        i3 = ""
        for j in i2:
            i3 = i3 + "+" + j
        i3 = i3.removeprefix("+")
        curUrl = urlPrefix + i3
        # print(curUrl)
        # parse url
        try:
            web = requests.get(curUrl, headers=headers).text
            soup = BeautifulSoup(web,"html.parser")
            # with open('codes.html','w', encoding="utf-8") as file:
            #     file.write(soup.prettify())
            target = soup.find_all('span')
            links = soup.find_all('a')
        except:
            print("error")
        purpose = "positionC"
        # Find related keywords ------------------------------------------
        if purpose == "keywords":
            n = 0
            for elem in target:
                if elem.text == "Related searches":
                    position = n
                n = n+1
            for m in range(position,len(target)):
                curTag = target[m]
                ch = "dir" in str(curTag)
                if ch == True:
                    curKey = curTag.text
                    relatedKeys.append(curKey)
                    # print(curKey)
            relatedKeys = set(relatedKeys)
            value = i.removesuffix("\n") + ":"
            for m1 in relatedKeys:
                value = value + "," +  m1
            w.write(value + "\r")
            relatedKeys = []
        # Find competitors ------------------------------------------
        elif purpose == "competitors":
            n = 0
            for elem in links:
                ch = "/url?q=" in str(elem)
                ch1 = "</span></span></a>" in str(elem)
                ch2 = "google.com" in str(elem)
                if ch == True and ch1==False and ch2==False:
                    e = re.findall(r"\bhttp.*?\b\/",str(elem))
                    if len(e)>0:
                        e = e[0]
                        e = e.removeprefix('http://').removeprefix('https://')
                        e = e.removeprefix('www.').removesuffix("/")
                        compLinks.append(e)
                    # print(elem)
            value = i.removesuffix("\n")
            for m1 in compLinks:
                value = value + "," +  m1
            w.write(value + "\r")
            compLinks = []
         # Find position (first page) of keywords ------------------------------------------
        elif purpose == "position":
            webSite = "top-packs.com"
            n = 0
            for elem in links:
                ch = "/url?esrc" in str(elem)
                ch1 = webSite in str(elem)
                ch2 = "</span></span></a>" in str(elem)
                if ch == True and ch2 == False:
                    n = n+1
                    if ch1 == True:
                        keyPo = n
                        break
            w.write(str(keyPo) + "\r")
            keyPo = 0
        # Find position (10-100) of keywords ------------------------------------------
        elif purpose == "positionC":
            webSite = "top-packs.com"
            n1 = 0
            for l in range(4,7):
                if n1 == 0:
                    n = 0
                    curUrl1 = curUrl + "&start="+ str(l*10)
                    web1 = requests.get(curUrl1).text
                    soup1 = BeautifulSoup(web1,"html.parser")
                    links1 = soup1.find_all('a')
                    for elem in links1:
                        ch = "/url?q=" in str(elem)
                        ch1 = webSite in str(elem)
                        ch2 = "</span></span></a>" in str(elem)
                        if ch == True and ch2 == False:
                            n = n+1
                            if ch1 == True:
                                keyPo = n + l*10
                                n1 = 1
                                break
            w.write(str(keyPo) + "\r")
            keyPo = 0

        # compare two competitors ------------------------------------------
        elif purpose == "compare":
            comp1 = "top-packs.com"
            comp2 = "sigolpack.com"
            n = 0
            n1 = 0
            n2 = 0
            for elem in links:
                ch = "/url?q=" in str(elem)
                ch1 = comp1 in str(elem)
                ch2 = comp2 in str(elem)
                ch3 = "</span></span></a>" in str(elem)
                if ch == True and ch3 == False:
                    n = n+1
                    if ch1 == True:
                        n1 = n
                    elif ch2 == True:
                        n2 = n
                if n1!=0 and n2!=0:
                    break
            value = "The position of " + comp1 + " is :" +str(n1) + " and the position of " + comp2 + " is :" +str(n2)      
            w.write(value + "\r")
        




if __name__ == "__main__":
  main();

