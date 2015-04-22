import csv
import itertools as it
import sys 
from relations import extractRelation
from tagger    import tagName

def loadNames(filename):
    with open(filename,"rb") as f:
        names = f.readlines()
        names = filter(lambda x: x != "null",names)
        names = map(lambda x: x[1:-1],names)
        return names
    
def main():
    inpt = sys.argv[1]
    inames = loadNames(inpt)
    
    for i in inames:
        try:
            i = extractRelation(i)
            tagName(i["name"])
            for k in ["AKA","FKA","OBO"]:
                if i["tag"] == k:
                    tagName(i[k.lower()+"_name"])
        except Exception:
            print "Cannot parse: "+i
if __name__ == "__main__":
    main()
