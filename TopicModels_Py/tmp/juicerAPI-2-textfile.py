# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 17:29:31 2015

@author: sylviatippmann
"""

import urllib2 
from json import load 

n = '100'
outlets = '&sources%5B%5D=160&sources%5B%5D=8&sources%5B%5D=41'
key = 'ZtGNiDhnYDsoSRA1GiJDHfs3KtnlgGox'
url = 'http://data.test.bbc.co.uk/bbcrd-juicer/articles?apikey='+ key + outlets +'&offset=0&size=' + n

try:
    f = urllib2.urlopen(url)
except urllib2.HTTPError, e:
    print e.fp.read()


json_obj = load(f)




with open('newsarticles.txt','w') as f:
    for story in json_obj['list']['story']:
        article = []
        for paragraph in story['textWithHtml']['paragraph']:
            article.append(paragraph['$text'])
        art = ' '.join(article).encode('utf-8')
        f.write(art+'\n')