import json, requests
import numpy

# The Times, Guardian, FT
outlets = '&sources%5B%5D=160&sources%5B%5D=8&sources%5B%5D=41'
# number of articles
n = '100'

url = 'http://developer:anicca@new.juicer.bbcnewslabs.co.uk/articles?recent_first=true'+ outlets +'&offset=0&size=' + n

resp = requests.get(url=url)
data = json.loads(resp.text)

articles = [x["body"] for x in data["hits"]]
articles[1]
articles

articles_01 = [a.replace('\n', ' ') for a in articles]

# save to numpy
numpy.save("articleList_100", articles_01)

# save to txt file, one article per line
numpy.savetxt('articleList_100_text.txt', articles_01, delimiter=" ", fmt="%s") 

