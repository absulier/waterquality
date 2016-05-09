from bs4 import BeautifulSoup
import urllib
import pandas as pd

df = pd.read_csv('SDWISUS.csv')


r1 = urllib.urlopen(df['sdwsis'][0].replace('&amp;','&'))
soup = BeautifulSoup(r1,'lxml')
tables=soup.find_all('table')
print tables
