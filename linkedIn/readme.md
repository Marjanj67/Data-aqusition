# scraping linkedIn data (job posts) using python
This project finds ads for a certain keyword in a certain location (toronto) and then scarpes and gathers details about that job ad. 
## The code


### Importing the libraries
```
from bs4 import BeautifulSoup
import requests
```


### The main function

```
def main():
    global  details , description, benefits
    GetUrls()
    # print(jobUrls)
    d = open('allData.txt','w', encoding="utf-8")
    headers = 'url'+ '-,' + 'title' +'-,' + 'company' +'-,' + 'location'+'-,' + 'Number of applicants' +'-,' + 'workplace type' +'-,' + 'posted date' +'-,' + 'seniority' +'-,' + 'benefits' + '-,' + 'description'
    d.write(headers +"\r")
    for j in jobUrls:
        webUrl = requests.get(j).text
        soup = BeautifulSoup(webUrl,'html.parser')
        s=open('html.html','w')
        s.write(str(soup.prettify("utf-8")))
        try: 
            title = soup.find('h1').text
            #  ------
            company = []
            company = soup.find(href=FindCompany)
            company = str(company).split('/company/')[1]
            company = company.split("?")[0]
            # -----
            allspans = soup.find_all(['span','figcaption'])
            details = []
            details = AnalyseSpans(allspans)
            j = j.split('?')[0]
            
            #  ---------benefit
            benefits = []
            # uls = soup.find_all('ul')
            # benefits = FindBenefits(uls)
            # benefits = str(benefits).removeprefix('<ul><li>').removesuffix('</li></ul>').replace('</li><li>','- ')
            data = str(j)+ '-,' + str(title) +'-,' + str(company) +'-,' + str(details['location'])+'-,' + str(details['Number of applicants']) +'-,' + str(details['workplace type']) +'-,' + str(details['posted date']) +'-,' + str(details['seniority']) +'-,' + str(benefits)


            # -------
            description=[]
            # alldivs = soup.find_all('div')
            # description = AnalyseDivs(alldivs)
            data += '-,' + str(description)

            d.write(data + "\r")
        except:
            print('error')

```


### Functions for finding the urls
```
def GetUrls():
    city = 'toronto'
    cityGeo = {'toronto':'100025096','markham':'102280801'}
    geoId = cityGeo[city]
    q = open('queries.txt','r')
    global jobUrls
    for i in q:
        url = "https://www.linkedin.com/jobs/search/?currentJobId=3340121435&geoId=" + str(geoId) +"&keywords=" + str(i)
        url = url.removesuffix('\n')
        webUrl = requests.get(url).text
        soup = BeautifulSoup(webUrl,'html.parser')
        soup.find_all(href=Mylinks)
        url2 ="https://www.linkedin.com/jobs/search/?currentJobId=3340121435&geoId=" + str(geoId) +"&keywords=" + str(i) + "&start=25"
        url2 = url2.removesuffix('\n')
        webUrl = requests.get(url2).text
        soup = BeautifulSoup(webUrl,'html.parser')
        soup.find_all(href=Mylinks)


def Mylinks(href):
    global jobUrls
    s = str(href).startswith('https://ca.linkedin.com/jobs/view/')
    if href !=None:
        href = href.split("?")[0]
        with open('processedUrl.txt', 'r') as f:
            urls_in_file = f.read().splitlines()
            if s==1 and href not in urls_in_file:
                jobUrls.append(href)


```
