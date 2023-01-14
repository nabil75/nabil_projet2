from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime

#Récupérer la position d'une sous-chaîne dans une chaîne de caractères
def get_substring_position(s, str, n):
    sep = s.split(str, n)
    if len(sep) <= n:
        return -1
    return len(s) - len(sep[-1]) - len(str)

#Récupérer les éléments de description d'un livre
def get_book_elements(url):
    descripteurs =[]
    descripteurs.append(url)
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'lxml')
    descripteurs.append(str(bs.find('table').find_all('tr')[0].find('td').text))
    descripteurs.append((bs.find('title').text).strip().replace(' | Books to Scrape - Sandbox',''))
    descripteurs.append(str(bs.find('table').find_all('tr')[3].find('td').text))
    descripteurs.append(str(bs.find('table').find_all('tr')[2].find('td').text))
    descripteurs.append(str(bs.find('table').find_all('tr')[5].find('td').text))
    descripteurs.append(bs.find('article',{'class':'product_page'}).find('p').text)
    descripteurs.append(str(bs.find('ul',{'class':'breadcrumb'}).find_all('li')[2].find('a').text))
    descripteurs.append(str(bs.find('table').find_all('tr')[6].find('td').text))
    #Récupérer l'url complète de l'image
    str_img = str(bs.find('div',{'class':'item active'}).find('img').attrs['src'])
    pos = get_substring_position(str_img, "/", 2)
    descripteurs.append("http://books.toscrape.com"+ str_img[pos:])
    #Télécharger image dans le répertoire courant
    img_to_dowload = requests.get("http://books.toscrape.com"+ str_img[pos:])
    path_img_file = os.getcwd()+"/"+str(bs.find('table').find_all('tr')[0].find('td').text)+".jpg"
    open(path_img_file, "wb").write(img_to_dowload.content)
    return descripteurs

#Pousser les données récupérées dans un fichier CSV
def push_data_to_csv(list_descripteurs):
    path_file = os.getcwd()+'\csv_file.csv'
    csv_file = open(path_file,'w+', newline='')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(('product_page_url', 'universal_ product_code (upc)','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url'))
    for descripteurs in list_descripteurs:
        writer.writerow((descripteurs[0], descripteurs[1], descripteurs[2], descripteurs[3], descripteurs[4], descripteurs[5], descripteurs[6], descripteurs[7], descripteurs[8], descripteurs[9]))
    csv_file.close()

# ================== récupérer un seul livre
now_begin = datetime.datetime.now()
print(str(now_begin.hour)+' h', str(now_begin.minute)+' min', str(now_begin.second)+' s')
path_file = os.getcwd()+'/csv_file1.csv'
url='http://books.toscrape.com/catalogue/choosing-our-religion-the-spiritual-lives-of-americas-nones_14/index.html'
list_descripteurs=[]
descripteurs = get_book_elements(url)
list_descripteurs.append(descripteurs)
push_data_to_csv(list_descripteurs)
now_end = datetime.datetime.now()
print(str(now_end.hour)+' h', str(now_end.minute)+' min', str(now_end.second)+' s')

