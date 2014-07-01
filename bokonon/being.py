from collections import defaultdict
import copy
from networkx import nx
import uuid
from Levenshtein import distance

being =      lambda : {"type": "Being"}
represents = lambda : {"relation":"represents"}

def addRecord(universe,record):
    rid = str(uuid.uuid1())
    bid = str(uuid.uuid1())    
    universe.add_node(bid,being())
    universe.add_node(rid,record)
    universe.add_edge(rid,bid,represents())
    return rid

def findBeing(universe,l):
    beings = []
    for lb,d in universe[l].iteritems():
        if d["relation"] == "represents":
            beings.append(lb)
            
    if len(beings) == 0:
        raise Exception("Cannot find a being for \"{}\"".format(l))
    elif len(beings) == 1:
        return beings[0]
    else:
        raise Exception("Found {} beings for {}: {}".format(len(beings),l,",".join(beings)))

def mergeTheirBeings(universe,al,bl):
    a = findBeing(universe,al)
    b = findBeing(universe,bl)        
    if a != b:
        for v in nx.neighbors(universe,b):
            universe.add_edge(v,a,represents())
            universe.remove_edge(v,b)
        av = universe.node[a]
        bv = universe.node[b]        
    return al

def cullHermits(universe):
    for (k,v) in universe.nodes(data=True):            
        if k in universe and v["type"] == "Being" and len(nx.neighbors(universe,k)) == 0:
            universe.remove_node(k)

def countTypes(universe):
    beings = filter(lambda x: x[1]["type"] == "Being", universe.nodes(data=True))
    d = defaultdict(lambda: 1)
    for b in beings:
        ns = nx.neighbors(universe,b[0])
        d[universe.node[ns[0]]["type"]] += 1
    return d
            
def groupMerge(universe, pred, extract,description=None):
    if description != None:
            print(description)        
            start = countTypes(universe)

    nodes = filter(lambda t: pred(t[1]),universe.nodes(data=True))
    d = defaultdict(list)
    for k,v in nodes:
        for s in extract(v):
            d[s].append(k)
    for k,v in d.iteritems():
        merged = reduce(lambda x,y: mergeTheirBeings(universe,x,y),v)
        
    cullHermits(universe)
    if description != None:
            d = countTypes(universe)
            txt = "" 
            for k,v in d.iteritems():
                txt += k + " " + str(v-start[k]) + " "
            print(txt)
            print("")

def windowMerge(universe, pred, extract, windowSize, maxDistance, description=None):
    if description != None:
            print(description)        
            start = countTypes(universe)

    nodes = filter(lambda t: pred(t[1]),universe.nodes(data=True))
    d = {}
    for k,v in nodes:
        for s in extract(v):
            d[s] = k
            
    items = sorted(d.iteritems(),key=lambda x: x[0])
    for i in range(0,len(items)-windowSize):
        a = items[i]        
        for j in range(1,windowSize+1):
            b = items[i+j]
            dQ = distance(a[0],b[0]) <= maxDistance
            bQ = findBeing(universe,a[1]) != findBeing(universe,b[1])
            lQ = len(a[0]) > 5 and len(b[0]) > 5 
            if  dQ and bQ and lQ:
                print(a[0])
                print(b[0])
                print("\n")
                mergeTheirBeings(universe,a[1],b[1])
                        
    cullHermits(universe)
    if description != None:
            d = countTypes(universe)
            txt = "" 
            for k,v in d.iteritems():
                txt += k + " " + str(v-start[k]) + " "
            print(txt)
            print("")

            
def matchTypeAndHasFields(t,fs):
    return lambda v: v["type"] == t and all([v[f] != "" for f in fs])
    
