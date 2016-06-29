import categoriser
from urllib2 import Request, urlopen, URLError
import json
import os,sys
import codecs
import time

reload(sys)
sys.setdefaultencoding("utf-8")

request = Request('http://juicer.api.bbci.co.uk/articles?q=%22london%22&recent_first=yes&api_key=<API_KEY>')

before = "2016-06-01"
after = "2016-01-01"
key = '<API_KEY>'
source = "&sources%5B%5D=1"

call = "http://juicer.api.bbci.co.uk/articles?recent_first=yes" + source + "&published_after=" + after + "T00:00:00.000Z" + "&published_before=" + before + "T00:00:00.000Z" + "&size=10" + "&api_key=" + key
print call

response = urlopen(call)
articleJSON = response.read()
result = json.loads(articleJSON)
hits = int(result['total'])

print hits

try:

	f = open('bbc-dataset-201601-201607-time.tab', 'a')
	size = 10 # default apparently, getting error with setting size in API call
	for offset in range(0, hits, size):
		call = "http://juicer.api.bbci.co.uk/articles?recent_first=yes" + source + "&published_after=" + after + "T00:00:00.000Z" + "&published_before=" + before + "T00:00:00.000Z" + "&api_key=" + key + "&offset=" + str(offset) + "&size=" + str(size)
		print call

		response = urlopen(call)
		articleJSON = response.read()
		result = json.loads(articleJSON)

		for a in range(0, size-1):
			#print a
			articleurl = result['hits'][a]['url']
			cat = categoriser.parse(articleurl)
			if cat:
				body = result['hits'][a]['body']
				body = body.replace('\n', ' ').replace('\r', '')
				body = body.encode('utf-8')

				title = result['hits'][a]['title']
				title = title.encode('utf-8')

				date = result['hits'][a]['published']

				f.write(str(cat) + "\t" + result['hits'][a]['url'] + "\t" + title  + "\t" + body + "\t" + date + "\n")

	
except URLError, e:
    print 'No kittenz. Got an error code:', e


print hits






