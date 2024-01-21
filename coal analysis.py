import requests 
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

wikiurl='https://en.wikipedia.org/wiki/List_of_countries_by_coal_production'
table_class='wikitable sortable jquery-tablesorter'

response=requests.get(wikiurl)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table',{'class':"wikitable"})

df_coalall = pd.read_html(str(table))[0]

list_country = ['Russia', 'Germany', 'Poland', 'Czech Republic',
                'Ukraine', 'Romania', 'Greece', 'Bulgaria']

df_coalpre = df_coalall[df_coalall['Country'].isin(list_country)]
df_coalpre = df_coalpre.iloc[:,0:2]
df_coalpre.rename(columns={'2020[1]':'2020'}, inplace=True)
df_coalpre.reset_index(drop=True, inplace=True)

df_coal = pd.melt(df_coalpre, id_vars=['Country'],
                  value_vars='2020',
                  var_name='Year', value_name='Value')

df_coal['Percent'] = [round(i*100/sum(df_coal.Value),1) for i in df_coal.Value]
print(df_coal)


pal_ = list(sns.color_palette(palette='plasma_r',
                              n_colors=len(list_country)).as_hex())

plt.figure(figsize=(14, 14))
plt.rcParams.update({'font.size': 16})
plt.pie(df_coal.Value,
        labels= df_coal.Country,
        colors=pal_, autopct='%1.1f%%',
        pctdistance=0.9)
plt.legend(bbox_to_anchor=(1, 1), loc=2, frameon=False)
plt.show()

df_select = df_coal[['Country', 'Percent']]
df_select['Label_color'] = [i for i in df_coal['Country']]

df_coalmod = df_coal[['Country']]
df_coalmod['Percent'] = [100-i for i in df_coal['Percent']]
df_coalmod['Label_color'] = ['Other countries']*len(list_country)

df_db = pd.concat([df_select, df_coalmod],axis=0)
df_db

color_country = dict(zip(list_country,pal_))
color_country['Other countries'] = '#b9b9b9'

df_ = df_select.iloc[0:2,:]
df_['Y'] = [1]*len(df_)

import plotly.express as px
fig = px.scatter(df_, x='Percent', y='Y', color='Label_color',
                 text = [str(i)+' %' for i in df_.Percent][0:len(df_)],
                 opacity=1,
                 color_discrete_map=color_country)

fig.update_layout(width = 950, height = 300, plot_bgcolor = 'white',
                  margin = dict(t=40, l=20, r=20, b=20),
                  yaxis={'categoryorder':'total descending'},
                  legend=dict(title='Countries'),
                  showlegend=True)

for c in list_country:
    df = df_[df_['Country']==c]
    fig.add_shape(type="line", layer="below",
                  line=dict(color='black', width=6),
                  y0=1, x0=list(df_.Percent)[0],
                  y1=1, x1=list(df_.Percent)[1])

fig.update_traces(textposition='top center', marker={'size':65},
                  textfont=dict(color='black'))
fig.update_yaxes(visible=False)
fig.update_xaxes(visible=True, showgrid =False, range=[-1, 101]) 

color_country = dict(zip(list_country,pal_))
color_country['Other countries'] = '#b9b9b9'

import plotly.express as px
fig = px.scatter(df_db, x='Percent', y='Country', color='Label_color',
                 text = [str(i)+' %' for i in df_db.Percent],
                 opacity=1,
                 color_discrete_map=color_country)

fig.update_layout(width = 950, height = 900, plot_bgcolor = 'white',
                  margin = dict(t=40, l=20, r=20, b=20),
                  yaxis={'categoryorder':'total descending'},
                  legend=dict(title='Countries'),
                  showlegend=True)

for c in list_country:
    df = df_db[df_db['Country']==c]
    fig.add_shape(type="line", layer="below",
                  line=dict(color=color_country.get(c), width=6),
                  y0=c, x0=list(df.Percent)[0],
                  y1=c, x1=list(df.Percent)[1])

fig.update_traces(textposition='top center', marker={'size':58},
                  textfont=dict(color='black'))
fig.update_yaxes(title='', visible=True, showgrid =False)
fig.update_xaxes(visible=False) 

import plotly.express as px
fig = px.scatter(df_db, x='Percent', y='Country', color='Label_color',
                 text = [str(i)+' %' for i in df_db.Percent],
                 size = 'Percent', size_max=45,
                 opacity=1,
                 color_discrete_map=color_country)

fig.update_layout(width = 950, height = 900, plot_bgcolor = 'white',
                  margin = dict(t=40, l=20, r=20, b=20),
                  yaxis={'categoryorder':'total descending'},
                  legend=dict(title='Countries'),
                  showlegend=True)

for c in list_country:
    df = df_db[df_db['Country']==c]
    fig.add_shape(type="line", layer="below",
                  line=dict(color=color_country.get(c), width=6),
                  y0=c, x0=list(df.Percent)[0],
                  y1=c, x1=list(df.Percent)[1])

fig.update_traces(textposition='top center',
                  textfont=dict(color='black'))

fig.update_yaxes(title='', visible=True, showgrid =False)
fig.update_xaxes(visible=False) 
fig.show()


