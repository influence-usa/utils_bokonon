from arpeggio.cleanpeg import ParserPEG
from arpeggio import PTNodeVisitor, visit_parse_tree

parser = ParserPEG(open("tagger.peg","r").read(),"parse",skipws=False,ignore_case=True)

class Visitor(PTNodeVisitor):
    def visit_parse(self,node,children):
        return children
    
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

def tagName(name):
    tree = parser.parse(name)
    parsedSeq = visit_parse_tree(tree, Visitor(defaults=False,debug=False))
    return parsedSeq
