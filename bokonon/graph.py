from being import groupMerge, countTypes, matchTypeAndHasFields
from load import loadData
from pprint import pprint
from save import steralize, save, project
from text import extractNames

def represent(v):
    l = ", ".join([v["name"],v["address"],v["city"],v["state"]])
    if "specific_issuse" in v:
        l += "\n"+v["specific_issues"]
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
    
    project(universe,"clientnames.txt", lambda v: v["type"] == "client", represent)

    
if __name__ == "__main__":
    main()
    
