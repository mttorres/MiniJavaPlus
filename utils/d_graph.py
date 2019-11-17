#CONSTRUIR GRAFO APÓS ARVORE OU ENQUANTO A MONTA ?

def graph_construct(astnode, DEP_GRAPH):
    for a in astnode.atributes:
        DEP_GRAPH.append(D_GraphNode(a))



class D_GraphNode:
    def __init__(self,atribute,type=None,depends=None,resolves=None):
            #self.type = type # pensei em por como tipo : value e functional (no livro ele divide os nós entre os que são "comandos" e os que são chamadas de função)
            #por enquanto vou deixar none
            self.atribute = atribute
            if depends:
                self.depends = list(filter(None, depends))
            else:
                self.children = []
            if resolves:
                self.resolves = list(filter(None, resolves))
            else:
                self.leaf = []

    def __str__(self):
        return "[DGraph_NODE]: %s" % (self.atribute) + " \n \t depends of : %s" % (self.depends) + "\n \t resolve: %s" % (self.resolves)