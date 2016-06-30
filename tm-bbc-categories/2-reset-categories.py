import sys
import re

# argv[0] = script
# argv[1] = test folder
 
IN = open('../data-from-Juicer/bbc-dataset-201601-201606.tab', 'r')
MAP = open('tests/'+ sys.argv[1] +'/categories_mapped.csv', 'r')
OUTSUB = open('tests/'+ sys.argv[1] +'/bbc-data-201601-201606_sub.tab', 'w')

def f3(seq):
   # Not order preserving
   keys = {}
   for e in seq:
       keys[e] = 1
   return keys.keys()

def report(mapping):
    v = []
    for i in D:
        v.append(D[i])

    print "original sections: " + str(len(v)-1) + "  >> unique sections: " + str(len(f3(v))-2)
    return len(f3(v))-1


# create a hashtable that hold the category mapping
D = {}
with MAP as m:
    for line in m:
        line = line.replace('\r\n','')
        splitline = re.split(',', line)
        D[splitline[0]] = splitline[1]

report(D)


a = 0
with IN as f:
    for line in f:
        
        line = line.strip()
        splitline = re.split(r'\t+', line)
        bbc_category = splitline[0]
        new_category = D[bbc_category]
 
        if(new_category!="-"):
            OUTSUB.write(line+"\t"+new_category+"\n")
            a = a+1

  
print "number of articles: " + str(a) 
