import csv
import itertools as it
import collections
import re
import json
from arpeggio.cleanpeg import ParserPEG
from arpeggio import *
import sys 

def loadNames(filename):
    with open(filename,"rb") as csvfile:
        reader = csv.DictReader(csvfile)
        names = set()
        print("Reading CSV")
        for row in reader:
        #for row in it.islice(reader,1,10000):
            names.add(row["name"])
        return names

def clean(s):
    s = s.strip().lower()
    s = re.sub('  ',' ',s)
    s = re.sub('#fedex ab#.*','fedexab',s)
    s = re.sub('\(amex\)','',s)
    s = re.sub('#fedex kinko\'s #.*','fedexkinko',s)
    s = re.sub('  ',' ',s)
    s = s.strip().lower()
    return s

#print test.parse("zack llc")

parser = ParserPEG(open("parser.peg","r").read(),"name",skipws=False)

class Visitor(PTNodeVisitor):
    def visit_name(self,node,children):
        return children
    def visit_token(self,node,children):
        return children[0]
    def visit_simple(self,node,children):
        return node.value
    def visit_special(self,node,children):
        return children[0]
    def visit_specialHelper(self,node,children):
        return children[0]
    def visit_corporates(self,node,children):
        return ""
    def visit_llc(self,node,children):
        return "LLC"
    def visit_and(self,node,children):
        return "AND"
    def visit_association(self,node,children):
        return "ASSOCIATION"
    def visit_national(self,node,children):
        return "NATIONAL"
    def visit_pllc(self,node,children):
        return "PLLC"
    def visit_llp(self,node,children):
        return "LLP"
    def visit_lp(self,node,children):
        return "LP"
    def visit_lpa(self,node,children):
        return "LPA"
    def visit_corporation(self,node,children):
        return "CORPORATION"
    def visit_limited(self,node,children):
        return "LIMITED"
    def visit_company(self,node,children):
        return "COMPANY"
    def visit_international(self,node,children):
        return "INTERNATIONAL"

def parseName(name):
    try:
        name = clean(name)
        tree = parser.parse(name+" ")
        # HACK CLUDGE: Using EOF as whitespace in a PEG
        # seems to cause a infinite loop of cache
        # hits. By putting a single whitespace at the
        # end of the name, parsing will complete and
        # still be accurate.
        canonical = visit_parse_tree(tree, Visitor(defaults=False))
        return " ".join(canonical).strip()
    except Exception:
        print "Cannot parse:",name

def parseNames(names):
    d = collections.defaultdict(set)
    for name in names:
        d[parseName(name)].add(name)
    return d

def saveDict(output,d):
    print("Saving names")
    for k,v in d.items():
        d[k] = list(v)
    with open(output,'w') as f:
        f.write(json.dumps(d,sort_keys=True,indent=4, separators=(',', ': ')))
        f.close()

if __name__ == "__main__":
    print sys.argv
    input,output = sys.argv[1:3] 
    names = loadNames(input)
    print(len(names))
    parsedNames = parseNames(names)
    saveDict(output,parsedNames)
