#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import urllib2
from os import path
from io import open
import socket

lines = []
urls = []
names = []
file_path = path.relpath('data/artists.txt')
with open(file_path, 'r', encoding='utf8') as a:
    for line in a:
        urls.append(unicode(line.split('\t')[2])+unicode('/+tags'))
        names.append(line.split('\t')[1])
with open('tags.txt', 'w', encoding='utf8') as a, open('tagsLog.txt', 'w', encoding='utf8') as b:
    for index, url in enumerate(urls):
        print(index)
        a.write('\n' + '#' + unicode(index) + '\t' + unicode(names[index]) + '\n')
        for i in range(10):
            try:
                page = urllib2.urlopen(url, timeout=10)
                soup = BeautifulSoup(page)
            except urllib2.URLError:
                b.write('Bad URL or timeout: ' + unicode(index) + '\t' + unicode(names[index]) + '\t' + unicode(url) + '\n')
                continue
            except socket.timeout:
                b.write('socket timeout: ' + unicode(index) + '\t' + unicode(names[index]) + '\t' + unicode(url) + '\n')
                continue
            break
        intro = soup.find_all(lambda tag: tag.name == 'a' and tag.get('rel') == ['tag'])
        if intro:
            for i in intro:
                lines = (unicode(i.get_text()).strip()).split('\n')
                for line in lines:
                    if line.strip():
                        a.write(line.strip() + '\n')
        else:
            b.write('empty get:\t' + unicode(index) + '\t' + unicode(names[index]) + '\t' + unicode(url) + '\n')