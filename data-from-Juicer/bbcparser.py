import re

class BbcParser:
   @staticmethod
   def parse(url):
      catlist = re.findall(r'([a-z]*)\-', url)
      return ('_'.join(catlist))
