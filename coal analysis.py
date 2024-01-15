import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

wikiurl='https://en.wikipedia.org/wiki/List_of_countries_by_coal_production'
table_class='wikitable sortable jquery-tablesorter'

response=requests.get(wikiurl)
#status 200: The server successfully answered the http request 
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table',{'class':"wikitable"})

list_country = ['Russia', 'Germany', 'Poland', 'Czech Republic',
                'Ukraine', 'Romania', 'Greece', 'Bulgaria']

df_coalall = pd.read_html(str(table))[0]
df_coalpre = df_coalall[df_coalall['Country'].isin(list_country)]
df_coalpre = df_coalpre.iloc[:,0:2]
df_coalpre.rename(columns={'2020[1]':'2020'}, inplace=True)
df_coalpre.reset_index(drop=True, inplace=True)
print(df_coalpre)