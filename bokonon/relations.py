from arpeggio.cleanpeg import ParserPEG
from arpeggio import PTNodeVisitor, visit_parse_tree

parser = ParserPEG(open("relations.peg","r").read(),"parse",skipws=False,ignore_case=True)

class Visitor(PTNodeVisitor):
    def visit_parse(self,node,children):
        return children
    
    def visit_splitter(self,node,children):
        return children[0]
    def visit_splitterHelper(self,node,children):
        return children[0]
    
    def visit_fka(self,node,children):
        return children[0]
    def visit_simpleFka(self,node,children):
        return ("FKA",node.value)
    def visit_abbrevFka(self,node,children):
        return ("FKA",node.value)
    def visit_complexFka(self,node,children):
        return ("FKA","".join(children))
    def visit_formers(self,node,children):
        return node.value
    def visit_verbs(self,node,chidlren):
        return node.value
    def visit_optional(self,node,children):
        return node.value
    
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

def extractRelation(name):
    tree = parser.parse(name)
    tokens = visit_parse_tree(tree, Visitor(defaults=False,debug=False))
    tag = None
    names = []
    i = ""
    for token in tokens:
        if isinstance(token,unicode):
            i += token
        elif tag == None:
            tag = token
            names.append(i)
            i = ""
        else:
            raise Exception("Too many relations in field")
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

    
works = False

try:
    extractRelation("a aka b fka c")
except Exception:
    works = True

if not works:
    raise Exception("extractRelation no longer throws an error when passed a field with multiple relations.")
