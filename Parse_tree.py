 
import nltk
import graphviz
from nltk import ChartParser
from nltk import CFG

from nltk.grammar import CFG
from nltk import RecursiveDescentParser


# Define the grammar
grammar1 = CFG.fromstring("""
    S -> NP VP
    NP -> Det N
    VP -> V NP
    Det -> 'the' | 'a'
    N -> 'cat' | 'dog'
    V -> 'chased' | 'ate'
""")
grammar= nltk.CFG.fromstring("""
    stmt -> assign_stmt | if_stmt | while_stmt | '{' stmts '}'
    stmts -> stmt recstmt | 
    recstmt -> stmts recstmt | 
                               
    assign_stmt -> id '=' expr ';'
                               
   if_stmt -> 'if' cond ':' stmt | 'if' cond ':' stmt 'else' stmt
                               
    while_stmt -> 'while' cond ':' stmt
                               
    cond -> id rel_op digit
                               
    rel_op -> '>' | '<' | '<=' | '>=' | '!=' | '=='
                               
     
    expr -> term R
    R -> '+' term R | '-' term R |
    term -> factor R1
    R1 -> '*' factor R1 | '/' factor R1 |
                                                   
    factor -> digit | id | '('expr')' | PI
    id -> letter recletter | digit recletter | '_' recletter | '$' recletter
    recletter -> id recletter | 
    letter -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
    digit -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    PI -> '3.14'
""")
#parser = ChartParser(CFG.grammar)
#parser = nltk.chartparse.ChartParser(grammar)
parser=RecursiveDescentParser(grammar)

# Define a sentence to parse
code = """ if x > 1 :
                x = 2 ; """  
sentence = code.split()

# Parse the sentence
trees = list(parser.parse(sentence))

# Check if there are any parse trees
if trees: # tree generated from parser

    tree = trees[0]

    #tree.draw()

    # Convert the parse tree to a dot file
    def tree_to_dot(tree):
        dot_str = "digraph G {\n"
        counter = 0

        def traverse(node, parent=None):
            nonlocal counter, dot_str
            node_id = counter
            counter += 1
            label = node if isinstance(node, str) else node.label()
            dot_str += f'  {node_id} [label="{label}"];\n'

            if parent is not None:
                dot_str += f'  {parent} -> {node_id};\n'

            if isinstance(node, nltk.Tree):
                for child in node:
                    traverse(child, node_id)

        traverse(tree)
        dot_str += "}\n"
        return dot_str


    # Get the dot format string
    dot_str = tree_to_dot(tree)

    # Create a Graphviz source object
    dot = graphviz.Source(dot_str)

    # Render the tree and save it to a file
    dot.render('parse_tree', format='png', view=True)

else:
    print("No parse tree found.")
'''
# Create a parser
parser = nltk.ChartParser(grammar1)

# Input sentence
#sentence = "the cat chased the dog"
sentence = " x = 3 ;"

# Parse the sentence
parser = parser.parse(sentence.split())

# Select the first parse tree
parse_tree = list(parser)

# Draw the parse tree using graphviz
def draw_parse_tree(tree):
    #dot = graphviz.Digraph()
    
    dot_str = tree_to_dot(tree)

    # Create a Graphviz source object
    dot = graphviz.Source(dot_str)

    # Render the tree and save it to a file
  
    #_draw_tree(dot, tree)
    #dot.format = 'png'
    dot.render('parse_tree',format = 'png', view=True)

def _draw_tree(dot, tree):
    if isinstance(tree, nltk.Tree):
        dot.node(str(tree), tree.label())
        for child in tree:
            if isinstance(child, nltk.Tree):
                dot.edge(str(tree), str(child))
                _draw_tree(dot, child)
            else:
                dot.node(str(child), str(child))
                dot.edge(str(tree), str(child))

draw_parse_tree(parse_tree)
#sentence = "the cat chased the dog"  '''
# Create a parser
 