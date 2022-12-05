# Getting data from google search engine
## Purpose of the data
this data is for marketing purposes and includes several parts:
* finding the position of a certain domain for a certain keyword in the search result
* Finding competior's position for a certain keyword
* Extracting related searches for a certain keyword

## Process of acquiring the data

### Importing required libraries
```
from pickle import UNICODE
import requests
from bs4 import BeautifulSoup
import re
```

### Defining global variables
```
# Global variables
UrlPrefix = "https://www.google.com/search?q="
headers = {  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'} 
```

### Main Function
```

def main():
    Urls = list_urls()  # Read keywords from a file and creates urls
    purpose = "competitors"  # There are five purposes: keywords,competitors, position, positionC, compare
    # Find related keywords ------------------------------------------
    if purpose == "keywords":
        AllRelatedKeywords = []
        for CurrentUrl in Urls:
            Soup = read_url(CurrentUrl) # Reads a url using beautifulsoap
            target = Soup.find_all('span')
            RelatedKeywords = find_similar_keywords(target) # Finds related keywords
            value = CurrentUrl + ":" + RelatedKeywords
            AllRelatedKeywords.append(value)
        write_to_file(AllRelatedKeywords)  # Write data in a file
    # Find competitors ------------------------------------------
    elif purpose == "competitors":
        AllCompetitors = [] 
        for CurrentUrl in Urls:
            Soup = read_url(CurrentUrl) # Reads a url using beautifulsoap
            links = Soup.find_all('a')
            CompetitorsLinks = find_competitors(links)
            value = CurrentUrl + ":" + CompetitorsLinks
            AllCompetitors.append(value)
        write_to_file(AllCompetitors)
    # Find position (first page) of keywords ------------------------------------------
    elif purpose == "position":
        WebSite = "top-packs.com"
        AllPositions = []
        for CurrentUrl in Urls:
            Soup = read_url(CurrentUrl) # Reads a url using beautifulsoap
            links = Soup.find_all('a')
            Position = find_position(links,WebSite)
            AllPositions.append(Position)
        write_to_file(AllPositions)
        # Find position (10-100) of keywords ------------------------------------------
    elif purpose == "positionC":
        WebSite = "top-packs.com"
        AllPositions = []
        for CurrentUrl in Urls:
            CheckPosition = 0
            for l in range(4,7):
                if CheckPosition == 0:
                    curUrl1 = CurrentUrl + "&start="+ str(l*10)
                    soup1 = read_url(curUrl1)
                    links1 = soup1.find_all('a')
                    Position = find_position(links1,WebSite)
                    if Position > 0:
                        CheckPosition = 1
            AllPositions.append(Position)
        write_to_file(AllPositions)

        # compare two competitors ------------------------------------------
    elif purpose == "compare":
        Competitor1 = "top-packs.com"
        Competitor2 = "sigolpack.com"
        Position1 = 0
        Position2 = 0
        AllCompetitorData = []
        for CurrentUrl in Urls:
            Soup = read_url(CurrentUrl) # Reads a url using beautifulsoap
            links = Soup.find_all('a')
            Position1 = find_position(links,Competitor1)
            Position2 = find_position(links,Competitor2)
            value = "The position of " + Competitor1 + " is :" +str(Position1) + " and the position of " + Competitor2 + " is :" +str(Position2)  
            AllCompetitorData.append(value)    
        write_to_file(AllCompetitorData)
```
### List url function
This function is used to create urls from list of keywords and returns a list of urls.

```
def list_urls():
    KFile = open("keyWords.txt",'r',encoding="utf-8")
    Urls = []
    for keyword in KFile:
        KeyParts = keyword.removesuffix("\n").split(" ")
        FinalKeyword = ""
        for Part in KeyParts:
            FinalKeyword = FinalKeyword + "+" + Part
        FinalKeyword = FinalKeyword.removeprefix("+")
        FinalUrl = UrlPrefix + FinalKeyword
        Urls.append(FinalUrl)
    return Urls
```
### Read url Function
This function reads content of a url using BeautifulSoup and returns the soup object.
```

def read_url(url):
    global headers
    Soup = []
    try:
        Web = requests.get(url, headers=headers).text
        Soup = BeautifulSoup(Web,"html.parser")
    except:
        print("error")
    return Soup
```
### Find similar keywords function
This function creates a string made of related keywords for each keyword and returns that string.
```

def find_similar_keywords(target):
    iter = 0
    RelatedKeys = []
    for elem in target:
        if elem.text == "Related searches":
            Position = iter
        iter += 1
    for i in range(Position,len(target)):
        CurrentTag = target[i]
        CheckIn = "dir" in str(CurrentTag)
        if CheckIn == True:
            CurrentKey = CurrentTag.text
            RelatedKeys.append(CurrentKey)
    RelatedKeys = set(RelatedKeys)
    RelatedKeywords = ''
    for key in RelatedKeys:
        RelatedKeywords = RelatedKeywords + "," +  key
    return RelatedKeywords
```


### Find competitors function
This function creates a list of competitors for a certain keyword  and returns them as a combined string.
```
def find_competitors(links):
    CompetitorsLinks = ''
    for elem in links:
        CheckIn = "/url?esrc=s" in str(elem)
        CheckIn1 = "</span></span></a>" in str(elem)
        CheckIn2 = "google.com" in str(elem)
        if CheckIn == True and CheckIn2 == False:
            Links = re.findall(r"\bhttp.*?\b\/",str(elem))
            if len(Links)>0:
                Links = Links[0]
                Links = Links.removeprefix('http://').removeprefix('https://')
                Links = Links.removeprefix('www.').removesuffix("/")
                CompetitorsLinks = CompetitorsLinks + ',' + str(Links)
    return CompetitorsLinks
```
### Find position function
This function finds position of a domain in search result for a specific keyword.
```
def find_position(links,WebSite):
    itet = 0
    Position = 0
    for elem in links:
        CheckIn = "/url?esrc" in str(elem)
        CheckIn1 = WebSite in str(elem)
        CheckIn2 = "</span></span></a>" in str(elem)
        if CheckIn == True and CheckIn2 == False:
            itet = itet+1
            if CheckIn1 == True:
                Position = itet
    return Position      

        


 
```
### Write to file function
This function writes data to a file
```
def write_to_file(data):
    w = open("data.txt",'w',encoding="utf-8")
    for d in data:
        w.write(str(d) + "\r")
```
## Output and results
The result is a text file name data that contains different data based on the chosen purpose.
