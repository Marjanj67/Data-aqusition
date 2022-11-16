import pandas as pd

# page url
url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'
data = pd.read_html(url,attrs={'class':'wikitable'})

# formating the data into dataframe
df = pd.DataFrame(data[0])

#saving data into a csv file
df.to_csv('data.csv',index=False)
