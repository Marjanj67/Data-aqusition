from bs4 import BeautifulSoup
import requests





jobUrls = []


def Mylinks(href):
    global jobUrls
    s = str(href).startswith('https://ca.linkedin.com/jobs/view/')
    if href !=None:
        href = href.split("?")[0]
        with open('processedUrl.txt', 'r') as f:
            urls_in_file = f.read().splitlines()
            if s==1 and href not in urls_in_file:
                jobUrls.append(href)

def FindCompany(href):
    global company
    if '/company/' in str(href):
        c = href.split('/company/')[1]
        c1 = c.split("?")[0]
        company = c1
        return company

def AnalyseSpans(spans):
    global  details
    location= []
    NumApp = []
    Wtype = []
    postedTime = []
    seniority = []
    for k in spans:
        # print(k)

        if "topcard__flavor topcard__flavor--bullet" in str(k):
            location = k.text.split('\n')[1].strip(' ')
        if "applicants" in str(k):
            if k.text != [] and k.text != '' :
                NumApp = k.text.split('\n')[1].strip(' ')
        if "workplace-type" in str(k):
            Wtype= k.text.split('\n')[1].strip(' ')
        if 'posted-time' in str(k):
            postedTime= k.text.split('>')[0].strip(' \n')
        if 'description__job' in str(k) and seniority==[]:
            seniority = k.text.split('\n')[1].strip(' ')
    details={'location':location,'Number of applicants': NumApp,'workplace type':Wtype,'posted date':postedTime,'seniority':seniority}
    return details

def AnalyseDivs(div):
    global description
    description = []
    sep = '<div class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5">'
    sep1 = 'Seniority level'
    sep3 = '\n \n<button aria-expanded="false"'
    tags = ['\n','<em>','</em>','</strong>','<p>','<br/>','</p>','<strong>','<u>','</u>','<li>','</li>','<ul>','</ul>','<div>','</div>','</section>','<section>','</button>']
    for k in div:
        if 'description__text' in str(k):
            tempDes = str(k).split(sep, 1)[1]
            tempDes = tempDes.split(sep1,1)[0]
            for t in tags:
                tempDes = tempDes.replace(t,' ')
            tempDes = tempDes.split(sep3,1)[0]
            
    description = tempDes
    return description

def FindBenefits(uls):
    global benefits
    for u in uls:
        if 'benefit' in str(u):
            benefits = u
            return benefits

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

if __name__ == "__main__":
  main();
