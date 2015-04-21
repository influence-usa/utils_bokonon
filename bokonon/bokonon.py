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

parser = ParserPEG(open("parser.peg","r").read(),"parse",skipws=False,ignore_case=True)

class Visitor(PTNodeVisitor):
    def visit_parse(self,node,children):
        return children
    
    def visit_splitter(self,node,children):
        return children[0]
    def visit_splitterHelper(self,node,children):
        return children[0]
    def visit_fka(self,node,children):
        return children[0]
    def visit_abbrevFka(self,node,children):
        return ("FKA",node.value)

    def visit_complexFka(self,node,children):
        print node,children
        return ("FKA","".join(children))
    def visit_formers(self,node,children):
        return node.value
    def visit_verbs(self,node,chidlren):
        return node.value
    def visit_optional(self,node,children):
        return node.value
    
    def visit_simpleFka(self,node,children):
        return ("FKA",node.value)
    def visit_aka(self,node,children):
        return ("AKA",node.value)
    def visit_obo(self,node,children):
        return ("OBO",node.value)

    def visit_name(self,node,children):
        return "".join(children)
    def visit_whitespace(self,node,children):
        return "".join(children)
    def visit_whites(self,node,children):
        return node.value
    def visit_simple(self,node,children):
        return node.value

def parseName(name):
    tree = parser.parse(name)
    tokens = visit_parse_tree(tree, Visitor(defaults=False,debug=False))
    tag = None
    names = []
    i = ""
    print tokens
    for token in tokens:
        if isinstance(token,unicode):
            i += token
        else:
            tag = token
            names.append(i)
            i = ""
    names.append(i)
    if tag != None:
        k = tag[0].lower()+"_name"
        return {"name": names[0],
                k: names[1],
                "tag": tag[0],
                "value": tag[1]}
    else:
        return {"name": names[0],
                "tag": "simple"}
