from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import csv
import os

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

#Récupérer tous les livres appartenant à une catégorie
def get_category_elements(url, category_all_descripteurs):
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'lxml')
    list_books = bs.findAll('li',{'class','col-xs-6 col-sm-4 col-md-3 col-lg-3'})
    for book in list_books:
        book_adr = str(book.find('a').attrs['href'])
        #Récupérer l'url complète de l'image
        pos = get_substring_position(book_adr, "/", 3)
        book_url = "http://books.toscrape.com/catalogue/"+ book_adr[pos:]
        descripteurs = get_book_elements(book_url)
        category_all_descripteurs.append(descripteurs)
    li_next = bs.find('li',{'class','next'})
    if(li_next is not None):
        pos_start = get_substring_position(url, "/",6)
        pos_end = get_substring_position(url, "/", 7)
        pos_start=pos_start+1
        category = url[pos_start:pos_end]
        next_button = bs.find('li',{'class','next'}).find('a')
        url_text = next_button.attrs['href']
        next_page = 'http://books.toscrape.com/catalogue/category/books/'+category+'/'+url_text
        category_all_descripteurs = get_category_elements(next_page, category_all_descripteurs)
    return category_all_descripteurs

#Récupérer tous les livres présentés sur le site
def get_all_books_elements(url):
    html = urlopen(url)
    bs = BeautifulSoup(html.read(),'lxml')
    list_category = bs.select("div > ul > li > ul > li > a")
    all_descripteurs =[]
    for category in list_category:
        category_descripteurs=[]
        # Création d'un répertoire pour regrpuper tous les fichiers générés pour la catégorie en cours
        directory = (category.text).strip()
        parent_dir = "C:/Users/nabil/OneDrive/Documents/openclassroom/Projet_02/ressources/all"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        os.chdir(path)
        category_url = "http://books.toscrape.com/"+category['href']
        category_descripteurs = get_category_elements(category_url, category_descripteurs)
        push_category_data_to_csv(category_descripteurs, (category.text).strip())
        os.chdir(parent_dir)

#Pousser les données récupérées dans un fichier CSV pour chacune des category
def push_category_data_to_csv(list_descripteurs, category):
    path_file = os.getcwd()+"/"+category+".csv"
    csv_file = open(path_file,'w+', newline='')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(('product_page_url', 'universal_ product_code (upc)','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url'))
    for descripteurs in list_descripteurs:
        writer.writerow((descripteurs[0], descripteurs[1], descripteurs[2], descripteurs[3], descripteurs[4], descripteurs[5], descripteurs[6], descripteurs[7], descripteurs[8], descripteurs[9]))
    csv_file.close()

# push_data_to_csv(list_descripteurs, path_file)

# ================== récupérer tous les livres
url ='http://books.toscrape.com/'
get_all_books_elements(url)