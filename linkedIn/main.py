from bs4 import BeautifulSoup
import requests
import re



def get_base_urls():
    city = 'toronto'
    cityGeo = {'toronto':'100025096','markham':'102280801'}
    geoId = cityGeo[city]
    q = open('queries.txt','r')
    BaseUrls = []
    for i in q:
        Url1 = "https://www.linkedin.com/jobs/search/?currentJobId=3340121435&geoId=" + str(geoId) +"&keywords=" + str(i)
        Url2 ="https://www.linkedin.com/jobs/search/?currentJobId=3340121435&geoId=" + str(geoId) +"&keywords=" + str(i) + "&start=25"
        BaseUrls.append(Url1)
        BaseUrls.append(Url2)

    return BaseUrls



def get_urls(BaseUrls):
    JobUrls= []
    for bu in BaseUrls:    
        webUrl = requests.get(bu).text
        soup = BeautifulSoup(webUrl,'html.parser')
        Links = soup.find_all('a', {'href': re.compile(r'https:\/\/ca\.linkedin\.com\/jobs\/view\/.+')})
        for li in Links:
            Splitlink = str(li).split('"')
            UrlTemp = [x for x in Splitlink if x.startswith('https')][0]
            JobUrls.append(UrlTemp)
    return JobUrls

def find_title(Soup):
    title = Soup.find('h1').text
    return title


def find_company(Soup):
    Company = []
    Links = Soup.find_all('a')
    for li in Links:
        if Company == []:
            SplitLinks = str(li).split('"')
            Company = [x for x in SplitLinks if x.startswith('https://ca.linkedin.com/company/')]
    if Company != []:
        Company = str(Company).split('/company/')[1]
        Company = Company.split("?")[0]
    return Company



def get_description(Soup):
    alldivs = Soup.find_all('div')
    description = []
    sep = '<div class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5">'
    sep1 = 'Seniority level'
    sep3 = '\n \n<button aria-expanded="false"'
    tags = ['\n','<em>','</em>','</strong>','<p>','<br/>','</p>','<strong>','<u>','</u>','<li>','</li>','<ul>','</ul>','<div>','</div>','</section>','<section>','</button>']
    for k in alldivs:
        if 'description__text' in str(k):
            tempDes = str(k).split(sep, 1)[1]
            tempDes = tempDes.split(sep1,1)[0]
            for t in tags:
                tempDes = tempDes.replace(t,' ')
            tempDes = tempDes.split(sep3,1)[0]
    description = tempDes
    return description

 





def write_to_file(Data):
    w = open('allData.txt','w', encoding="utf-8")
    for d in Data:
        w.write(d +"\r")


def get_details(Soup):
    AllSpans = Soup.find_all('span')
    Location= []
    NumApp = []
    Wtype = []
    postedTime = []
    seniority = []
    for k in AllSpans:
        # print(k)
        if "topcard__flavor topcard__flavor--bullet" in str(k):
            Location = k.text.split('\n')[1].strip(' ')
        if "applicants" in str(k):
            if k.text != [] and k.text != '' :
                NumApp = k.text.split('\n')[1].strip(' ')
        if "workplace-type" in str(k):
            Wtype= k.text.split('\n')[1].strip(' ')
        if 'posted-time' in str(k):
            postedTime= k.text.split('>')[0].strip(' \n')
        if 'description__job' in str(k) and seniority==[]:
            seniority = k.text.split('\n')[1].strip(' ')
    
    uls = Soup.find_all('ul')
    for u in uls:
        if 'benefit' in str(u):
            benefits = u
    benefits = str(benefits).removeprefix('<ul><li>').removesuffix('</li></ul>').replace('</li><li>','- ')
    details={'location':Location,'Number of applicants': NumApp,'workplace type':Wtype,'posted date':postedTime,'seniority':seniority,'benefits':benefits}
    return details


def main():
    Data = []
    BaseUrls = get_base_urls()
    JobUrls = get_urls(BaseUrls)
    iter = 0
    header = 'url'+ '-,' + 'title' +'-,' + 'company' +'-,' + 'location'+'-,' + 'Number of applicants' +'-,' + 'workplace type' +'-,' + 'posted date' +'-,' + 'seniority' +'-,' + 'benefits' + '-,' + 'description'

    Data[iter] = header
    for j in JobUrls:
        webUrl = requests.get(j).text
        Soup = BeautifulSoup(webUrl,'html.parser')
        # s=open('html.html','w')
        # s.write(str(Soup.prettify("utf-8")))
        title = find_title(Soup)
        company = find_company(Soup)
        details = get_details(Soup)
        description = get_description(Soup)
        
        j = j.split('?')[0]
        Data[iter] = str(j)+ '-,' + str(title) +'-,' + str(company) +'-,' + str(details['location'])+'-,' + str(details['Number of applicants']) +'-,' + str(details['workplace type']) +'-,' + str(details['posted date']) +'-,' + str(details['seniority']) +'-,' + str(details['benefits']) + str(description)
        iter += 1
    write_to_file(Data)


if __name__ == "__main__":
  main();

