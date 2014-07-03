import codecs
import json
import multiprocessing
import networkx as nx
import os
import pickle
import re

from being  import addRecord, countTypes, groupMerge, matchTypeAndHasFields, windowMerge
from glob   import glob
from pprint import pprint
from save   import project, steralize, save
from text   import preProcess, extractNames

processed_files = 'processed_files'
processed_graph = 'processed_graph'

def carefulDict(jOb,d,props):
    for k,kvs in props:
        v = jOb
        found = True
        for vs in kvs:
            if vs in v:
                v = v[vs]
            else:
                found = False
                break
        if found:
            d[k] = preProcess(v)

corruption = "{http://www.PureEdge.com/XFDL/Custom}"

def clean(d):
    nd = {}
    for k,v in d.iteritems():
        nk = k.split(corruption)[-1]
        if type(v) == dict: ##TODO: map over arrays
            v = clean(v)
        nd[nk] = v
    return nd
            
    
def loadForm(f,t):
    t = str(t)
    jOb = {}
    fo = codecs.open(f,"r",encoding="utf-8")
    jOb = json.loads(fo.read())
    fo.close()
    if corruption+u'LOBBYINGDISCLOSURE{}'.format(t) in jOb:
        jOb = clean(jOb)

    try:
        jOb = jOb[u'LOBBYINGDISCLOSURE{}'.format(t)]
    except KeyError:
        print("Weird, flipping form number just in case")
        jOb = jOb[u'LOBBYINGDISCLOSURE{}'.format(str(3-int(t)))]        

    client = {        
        #Type
        "type":"client",
        "filename": f
    }

    #PRINCIPAL might be a way of getting around the brokers     
    carefulDict(
        jOb,client,
        [("name",["clientName"]),         
         ("address",["updates","clientAddress"]),
         ("city",   ["updates","clientCity"]),
         ("country",["updates","clientCountry"]),
         ("state",  ["updates","clientState"]),
         ("zip",    ["updates","clientZip"]),        
         ("address",["clientAddress"]),
         ("city",   ["clientCity"]),
         ("country",["clientCountry"]),
         ("state",  ["clientState"]),
         ("zip",    ["clientZip"]),
         ("description", ["clientGeneralDescription"]),
         ("specific_issuse", ["specific_issuse"])])


    firm = {
        #Type
        "type":"firm",
        "filename": f
    }
    
    carefulDict(
        jOb,firm,
        [("firstname",   ["firstName"]),
         ("lastname",    ["lastName"]),
         ("orgname",     ["organizationName"]),
         ("printedname", ["printedName"]),        
         ("address1",    ["address1"]),
         ("address2",    ["address2"]),        
         ("city",        ["city"]),
         ("country",     ["country"]),
         ("state",       ["state"]),
         ("zip",         ["zip"]),
         ("p_city",      ["principal_city"]),
         ("p_country",   ["principal_country"]),
         ("p_state",     ["principal_state"]),
         ("p_zip",       ["principal_zip"])])
    
    #Relationship
    #"houseID", "senateID", "specific_issues","alis"
    employs = {
        #actual data
        "relation": "employs",
        "houseID":     preProcess(jOb["houseID"]),
        "senate":      preProcess(jOb["senateID"]),
    }
    lobbyists = []
    if "lobbyists" in jOb:
        for l in jOb["lobbyists"]:
            if "lobbyistFirstName" in l and l["lobbyistFirstName"] != "":
                lobbyists.append({"firstname": l["lobbyistFirstName"],
                                  "lastname":  l["lobbyistLastName"],
                                  "suffix":    l["lobbyistSuffix"],
                                  "position":  l["coveredPosition"],
                                  "type": "lobbyist",
                                  "filename":  f})

    return (client, firm, employs, lobbyists)

def loadForm1(x):
    return loadForm(x,1)

def loadForm2(x):
    return loadForm(x,2)

def loadData():    
    if os.path.exists(processed_graph):
        print("Processed graph has been saved, reading that instead")
        with open(processed_graph,"r") as f:
            return pickle.load(f)
        
    else:
        universe = nx.Graph()    
        print("Loading and processing files now")
        p = multiprocessing.Pool(8)
        data  = p.map(loadForm1,glob(os.environ["HOUSEXML"]+"/LD1/*/*/*.json"))
        data += p.map(loadForm2,glob(os.environ["HOUSEXML"]+"/LD2/*/*/*.json"))    
        
        print("Starting from {} records".format(len(data)))
        print("Building universe")
        for col in data:
            if col == None:
                continue
            (client,firm,employs,lobbyists) = col
            if client["name"] == "":
                continue

            cid = addRecord(universe,client)
            fid = addRecord(universe,firm)
            universe.add_edge(fid,cid,employs)
            for l in lobbyists:
                lid = addRecord(universe,l)
                universe.add_edge(lid,fid,{"relation":"workedfor"})
            
        print("Universe loaded and built, saving now")
        with open(processed_graph,"w") as f:
            pickle.dump(universe,f,2)
        return universe
    
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
