from bs4 import BeautifulSoup, element
import numpy as np
import pandas as pd
import requests
import time
import unidecode
from itertools import cycle
from datetime import datetime
from lxml.html import fromstring
from requests.exceptions import ConnectionError, Timeout, ProxyError, RequestException
from urllib3.exceptions import ProtocolError
import sys
import os

sys.setrecursionlimit(10000)
proxy_enabled = True

def get_proxies(x):
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    time.sleep(1)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:x + 1]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies
def get_keywords():
    global url
    print("Introducir término clave: ")
    keyword1 = input()
    print("Desea introducir un segundo término (Y/N): ")
    respuesta = input()

    if respuesta == "Y" or respuesta == "y" or respuesta == "Yes" or respuesta == "yes":
        print("Introducir segundo término: ")
        keyword2 = input()
        url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=' + str(keyword1) + '+AND+' + str(keyword2)
    elif respuesta == "N" or respuesta == "n" or respuesta == "No" or respuesta == "no":
        url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=' + str(keyword1)
def parse_url(df, n, url, proxy_origin):
    global response

    if proxy_origin is None:
        while True:
            try:
                response = requests.get(url)
                time.sleep(1)
                print("Successful Connection: PubMed")
                break
            except:
                print("Retrying connection through IP")
    else:
        proxy_pool = cycle(proxy_origin)
        proxy = next(proxy_pool)
        while True:
            try:
                response = requests.get(url, proxies={"http": proxy, "https": proxy})
                time.sleep(1)
                print('Successful Connection: Pubmed')
                break
            except:
                print("Skipping. Connnection error. Proxy: ", proxy)
                proxy = next(proxy_pool)

    global soup

    soup = BeautifulSoup(response.text, "html.parser")
    searchbox = soup.findAll("div", {"class": "rprt"})


    for i in range(n):
        df.loc[i, 'Article'] = searchbox[i].a.string
        df.loc[i, 'Url'] = searchbox[i].a.get('href')
        df.loc[i, 'Status'] = 0
def get_abstract(url, proxy_origin, counter):
    global response

    if proxy_origin is None:
        while True:
            try:
                response = requests.get(url)
                time.sleep(1)
                print("Successful Connection: PubMed")
                break
            except:
                print("Retrying connection through IP")
    else:
        proxy_pool = cycle(proxy_origin)
        proxy = next(proxy_pool)
        while True:
            try:
                response = requests.get(url, proxies={"http": proxy, "https": proxy})
                time.sleep(1)
                print('Successful Connection: Pubmed')
                break
            except:
                print("Skipping. Connnection error. Proxy: ", proxy)
                proxy = next(proxy_pool)

    sub_soup = BeautifulSoup(response.text, "html.parser")
    titlebox = sub_soup.find("div", {"class": "rprt abstract"}).findAll("h1")

    if articles.loc[counter, "Article"] is None:
        articles.loc[counter, "Article"] = titlebox[0].string
        print("Finishing saving the name of article..." + str(counter + 1))

    authorbox = sub_soup.findAll("div", {"class": "auths"})

    articles.loc[counter, "Authors"] = authorbox[0].a.string.strip()
    print("Finishing saving the name of the author of article..." + str(counter + 1))

    abstractbox = sub_soup.find("div", {"class": "abstr"}).findAll("p")

    articles.loc[counter, "Abstract"] = abstractbox[0].string
    print("Finishing saving the abstract of article..." + str(counter + 1))

    if articles.loc[counter, "Article"] is None or articles.loc[counter, 'Abstract'] is None:
        articles.loc[counter, "Status"] = 0
    else:
        articles.loc[counter, "Status"] = 1
def save_abstracts(df, name):
    print("Do you wish to save to csv file? (Y/N): ")
    respuesta = input()

    if respuesta == "Y" or respuesta == "y" or respuesta == "Yes" or respuesta == "yes":
        filename = datetime.now().strftime(name + '-%Y-%m-%d-%H-%M.csv')
        df.to_csv(filename, sep=",", encoding='utf-8', index=False)
        print('Dataframe has been saved as ' + filename)
    elif respuesta == "N" or respuesta == "n" or respuesta == "No" or respuesta == "no":
        print("Dataframe has not been saved")
def proxie_des():
    print("Do you wish to enable proxies for your project? (Y/N)")
    x = input()
    print("How many articles do you wish to scrape? (Number)")
    y = input()
    if x == "YES" or x == "Yes" or x == "yes" or x == "Y" or x == "y":
        get_keywords()
        proxies = get_proxies(10)
        print(proxies)
        parse_url(articles, n=int(y), url=url, proxie_origin=proxies)
    elif x == "NO" or x == "No" or x == "no" or x == "N" or x == "n":
        get_keywords()
        proxies = None
        parse_url(articles, n=int(y), url=url, proxy_origin=proxies)

article = []
articles = pd.DataFrame(article, columns=["Article", "Url", "Authors", "Abstract", "Status"])

proxie_des()

print("Do you wish to enable proxies for abstract extration? (Y/N)")
z = input()
if z == "YES" or z == "Yes" or z == "yes" or z == "Y" or z == "y":
    for i in range(len(articles)):
        url2 = 'https://www.ncbi.nlm.nih.gov' + str(articles.loc[i, 'Url'])
        proxies = get_proxies(10)
        print(proxies)
        get_abstract(url2, proxies, i)
elif z == "NO" or z == "No" or z == "no" or z == "N" or z == "n":
    for i in range(len(articles)):
        url2 = 'https://www.ncbi.nlm.nih.gov' + str(articles.loc[i, 'Url'])
        proxies = None
        get_abstract(url=url2, proxy_origin=proxies, counter=i)

save_abstracts(articles, 'complete_abstracts')
