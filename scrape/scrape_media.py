from lxml import etree
import requests
import urllib.request


from bs4 import BeautifulSoup

medialinks = {}


def add2Dictionary(key, value):
    medialinks[key] = value


def fetchMediaLinks(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    data = soup.findAll('a')

    header = soup.find('h1')

    title = header.text.split("/")
    title = title[-2]
    key = title
    for media in data:

        if media['href'].endswith('/') and media.text != '../':
            fetchMediaLinks(url + media.text)


        elif media['href'] != '../':
            val = media['href']
            add2Dictionary(key, url + val)


def adddirectlinks(val, url):
    add2Dictionary(urllib.parse.unquote(val[:-4]), url)



url = 'http://130.185.144.102/Movies/'
parentResponse = requests.get(url)
parentSoup = BeautifulSoup(parentResponse.text, 'lxml')
mainLoad = parentSoup.findAll('a')

for mainlinks in mainLoad:
    r = mainlinks['href']
    if r.endswith('/') and (mainlinks.text != '../' and mainlinks.text != '[To Parent Directory]'):
        fetchMediaLinks(url + mainlinks.text)

    else:
        if mainlinks.text != '../' and mainlinks.text != '[To Parent Directory]':
            adddirectlinks(mainlinks.text, url + mainlinks.text)

#print(medialinks)

with open('C:\\Users\\prati\\Desktop\\BigList.m3u', 'w+') as f:
    f.write('#EXTM3U')
    f.write("\n")
    counter=1
    for key in medialinks:
        counter += 1
        f.write("\n")
        f.write('#EXTINF:-'+str(counter)+','+key)
        f.write("\n")
        f.write(medialinks[key])
''' for key  in medialinks:
    print(key)
    print(medialinks[key])'''
print("Process completed")