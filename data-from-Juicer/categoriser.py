import re
from bbcparser import BbcParser

def parse(url):
    bbc = re.compile("http://www.bbc.co.uk/news/")
    if (bbc.match(url)):
        return BbcParser.parse(url)
    else:
        return None
