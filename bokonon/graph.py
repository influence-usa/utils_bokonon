from being import  countTypes, groupMerge, matchTypeAndHasFields, windowMerge
from load import loadData
from pprint import pprint
import re
from save import project, steralize, save
from text import extractNames

def represent(v):
    l = ", ".join([v["name"],v["address"],v["city"],v["state"]])
    return l

def main():
    print("Loading universe...")
    universe = loadData()

    groupMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda v: [v["name"]],
               description="Merged clients based on exact name match")

    groupMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda v: extractNames(v["name"]),
               description="Merged clients based on extracted and cleaned name match")

    groupMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda v: [re.sub(" ","",v["name"])],
               description="Merged clients based on exact match without spaces",
               logging=represent)
    
    windowMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda v: extractNames(v["name"]),
                5,
                1,
               description="Merged clients based on windowed extracted name matchs")
    
    project(universe,"clientnames.txt", lambda v: v["type"] == "client", represent)

    
if __name__ == "__main__":
    main()
    
