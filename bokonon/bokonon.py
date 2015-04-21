import csv
import itertools as it
import collections
import re
import json
from arpeggio.cleanpeg import ParserPEG
from arpeggio import PTNodeVisitor, visit_parse_tree
import sys 

def loadNames(filename):
    with open(filename,"rb") as csvfile:
        reader = csv.DictReader(csvfile)
        names = set()
        print("Reading CSV")
        for row in reader:
        #for row in it.islice(reader,1,100):
            names.add(row["name"])
        return names

def clean(s):
    s = s.strip().lower()
    s = re.sub('  ',' ',s)
    return s

parser = ParserPEG(open("parser.peg","r").read(),"parse",skipws=False,ignore_case=True)

class Visitor(PTNodeVisitor):
    def visit_parse(self,node,children):
        return children
    
    def visit_splitter(self,node,children):
        return children
    def visit_splitterHelper(self,node,children):
        return children[0]
    def visit_fka(self,node,children):
        return children[0]
    def visit_abbrevFka(self,node,children):
        return ("FKA",node.value)
    def visit_complexFka(self,node,children):
        return ("FKA",node.value)
    def visit_simpleFka(self,node,children):
        return ("FKA",node.value)
    def visit_aka(self,node,children):
        return ("AKA",node.value)
    def visit_obo(self,node,children):
        return ("OBO",node.value)

    def visit_name(self,node,children):
        return children
    def visit_namePart(self,node,children):
        return children[0]
    def visit_simple(self,node,children):
        return ("SIMPLE",node.value)
    def visit_special(self,node,children):
        return children[0]
    def visit_specialHelper(self,node,children):
        return children[0]
    def visit_corporates(self,node,children):
        return children[0]
    def visit_llc(self,node,children):
        return ("LLC",node.value)
    def visit_and(self,node,children):
        return ("AND",node.value)
    def visit_association(self,node,children):
        return ("ASSOCIATION",node.value)
    def visit_national(self,node,children):
        return ("NATIONAL",node.value)
    def visit_pllc(self,node,children):
        return ("PLLC",node.value)
    def visit_llp(self,node,children):
        return ("LLP",node.value)
    def visit_lp(self,node,children):
        return ("LP",node.value)
    def visit_lpa(self,node,children):
        return ("LPA",node.value)
    def visit_corporation(self,node,children):
        return ("CORPORATION",node.value)
    def visit_limited(self,node,children):
        return ("LIMITED",node.value)
    def visit_company(self,node,children):
        return ("COMPANY",node.value)
    def visit_international(self,node,children):
        return ("INTERNATIONAL",node.value)

def collectTokens(seq):
    ob = {"tag" : None}
    col = []
    for i in range(0,len(seq)):
        s = seq[i]
        if s[0][0]in ["FKA","OBO","AKA"]:
            ob["tag"] = s[0]
            ob["first"] = col
            ob["second"] = collectTokens(seq[(i+1):])
            break
        else:
            col.append(s)
    if ob["tag"] == None:
        ob["tag"] = "name"
        ob["first"] = col
    return ob

def parseName(name):
    try:
        name = clean(name)
        tree = parser.parse(name+" ")
        # HACK CLUDGE: Using EOF as whitespace in a PEG
        # seems to cause a infinite loop of cache
        # hits. By putting a single whitespace at the
        # end of the name, parsing will complete and
        # still be accurate.
        parsedSeq = visit_parse_tree(tree, Visitor(defaults=False,debug=True))
        return parsedSeq
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

def aliasTable():
    inpt,outpt = sys.argv[1:3] 
    inames = loadNames(inpt)
    parsedNames = parseNames(inames)
    saveDict(outpt,parsedNames)
    print sys.argv

def collectedName(name):
    return collectTokens(parseName(name))

if __name__ == "__main__":
    aliasTable()
