from being import  countTypes, groupMerge, matchTypeAndHasFields, windowMerge
from load import loadData
from pprint import pprint
import re
from save import project, steralize, save
from text import extractNames

def represent(i,v):
    l = ", ".join([v["name"],v["address"],v["city"],v["state"]])
    return l

def main():
    print("Loading universe...")
    universe = loadData()

    #Solid matching
    groupMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda i,v: [v["name"]],
               description="Merged clients based on exact name match")

    #Surprisingly solid
    groupMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda i,v: [re.sub(" ","",v["name"])],
               description="Merged clients based on exact match without spaces")

    #Solid
    groupMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda i,v: [re.sub("'","",v["name"])],
               description="Merged clients based on exact match without 's")

    #Most likely solid
    groupMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda i,v: extractNames(v["name"]),
               description="Merged clients based on extracted and cleaned name match"
               )

    #Not so bad
    windowMerge(universe,
               matchTypeAndHasFields("client",["name"]),               
               lambda v: extractNames(v["name"]),
                5,
                1,
                pred=lambda v,w: v["state"] == w["state"] and v["city"] == w["city"] and v["address"] == w["address"],
                description="Merged clients based on windowed extracted name matchs")
    
    project(universe,"clientnames.txt", lambda v: v["type"] == "client", represent)

    groupMerge(universe,
               matchTypeAndHasFields("lobbyist",["firstname","lastname"]),
               lambda i,v: [(v["firstname"].lower(),v["lastname"].lower())],
               description="Merged lobbyists based on exact name match")

    def repper(i,v):
        fid = filter(lambda x: x[2]['relation'] == "workedfor",universe.edges([i],data=True))[0][1]
        return (v["lastname"]+", "+v["firstname"]+":"+universe.node[fid]["orgname"]).lower()
    
    project(universe,"lobbyistnames.txt", lambda v: v["type"] == "lobbyist",repper)
    
    
if __name__ == "__main__":
    main()    
