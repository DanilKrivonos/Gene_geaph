# Idea of this project is to make graph structure of genome more clear and more readable. Gene graph uses synteny blocks as nodes.

## Mauve_backboner

Use this to make backbone file from mauve.

### Pars_mauve 

To find syntheny blocks, we uses programm mauve .To make file for mauve  more clear ( make matrix.txt file for Gene_graph_maker.py).*.txt file has type *[sbi sbi+1 gn len1 len2 coordinate1 coordinate2]* lenmax*

#### Gene_graph_maker.py

The utiles, wich uses to make graph structure and .dot file. It takes .txt files attribute (example fo type of file evirt4matrix.txt). Script gives two files .dot and .png (exmple evirt4dot.dot and evirt4graph.png).
