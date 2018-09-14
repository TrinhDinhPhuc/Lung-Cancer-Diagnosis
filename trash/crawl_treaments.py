from bs4 import BeautifulSoup
import requests
import re
website_url = requests.get("https://www.cancer.org/cancer/small-cell-lung-cancer/treating/by-stage.html").text
soup = BeautifulSoup(website_url,'lxml')
all_texts = (soup.find('div',{'class':'col-md-9 col-sm-12'}))
_list=[2,3,4,5,6,7]
states_dict = {(all_texts.find_all('h3')[0].text):list(map(lambda a:all_texts.find_all('p')[a].text,_list))}
_list=[6,7,8,9,10,11,12]
states_dict[(all_texts.find_all('h3')[1].text)] = list(map(lambda a: all_texts.find_all('p')[a].text,_list))

print(states_dict)