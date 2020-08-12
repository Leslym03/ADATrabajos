import sys
import time
import graphviz as gv

DICTIONARY = "DICTIONARY.txt"

class Estado:
    NextId = 0
    
    def __init__(self):
        self.id = Estado.NextId
        Estado.NextId += 1
        self.final = False
        self.aristas = {}
        self.altura = 0
        self.count = 0

    def __str__(self):        
        arr = []
        if self.final: 
            arr.append("1")
        else:
            arr.append("0")

        for (etiqueta, node) in self.aristas.items():
            arr.append( etiqueta )   
            arr.append( str( node.id ) ) 

        return "_".join(arr)

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def numAltura(self):
        if self.final:
            return self.altura
        else:
            altura +=1

        for etiqueta, node in self.aristas.items():
            altura += node.numAltura()

        self.altura = altura
        return altura

    
    def reenumerar(sefl ,node , altura, idnode):
        if node.altura != altura:
            node.altura = altura
            node.id= idnode
            idnode += 1
        return self.node.id 

    def numAccesible(self):
        if self.count: 
            return self.count

        count = 0
        if self.final: 
            count += 1

        for etiqueta, node in self.aristas.items():
            count += node.numAccesible()

        self.count = count
        return count

class Dawg:
    def __init__(self):
        self.palAnterior = ""
        self.root = Estado()
        self.noVerificados = []
        self.nodosMinimizados = {} 

    def insert( self, palabra ):
        prefijoComun = 0
        for i in range( min( len( palabra ), len( self.palAnterior ) ) ):
            if palabra[i] != self.palAnterior[i]: 
                break
            prefijoComun += 1

        self._minimizar( prefijoComun )

        if len(self.noVerificados) == 0:
            node = self.root
        else:
            node = self.noVerificados[-1][2] 

        for letra in palabra[prefijoComun:]:
            nextNode = Estado()
            node.aristas[letra] = nextNode
            self.noVerificados.append( (node, letra, nextNode) )
            node = nextNode

        node.final = True      
        self.palAnterior = palabra  

    def finish( self ):
        self._minimizar( 0 );
        self.root.numAccesible()

    def _minimizar( self, downTo ):
        for i in range( len(self.noVerificados) - 1, downTo - 1, -1 ):
            (padre, letra, hijo ) = self.noVerificados[i];
            if hijo in self.nodosMinimizados:
                padre.aristas[letra] = self.nodosMinimizados[hijo]
            else:
                self.nodosMinimizados[hijo] = hijo;
            self.noVerificados.pop()

    def nodosCount( self ):
        return len(self.nodosMinimizados)

    def aristasCount( self ):
        count = 0
        for node in self.nodosMinimizados:
            count += len(node.aristas)
        return count

    def display(self):
        trans=[]
        estados=[]
        terminal=[]
        inicial = ["0"]
        alf = [chr(chNum) for chNum in list(range(ord('a'),ord('z')+1))]
        stack = [self.root]
        done = set()
        while stack:
            node = stack.pop()
            if node.id in done: 
                continue
            done.add(node.id)
            if node.final == True:
                terminal.append(str(node.id))
            print("{}: ({})".format(node.id, node))
            estados.append(str(node.id))
            for etiqueta, hijo in node.aristas.items():
                trans.append((node.id,hijo.id,etiqueta))
                print("    {} - {}".format(etiqueta, hijo.id))
                stack.append(hijo)
        dawg.draw(alf, estados, inicial, trans, terminal)

    def draw(self,alfabeto, estados, inicio, trans, final):
        g = gv.Digraph(format='svg')
        g.graph_attr['rankdir'] = 'TB'
        g.node('ini', shape="point")
        for e in estados:
            if e in final:
                g.node(e, shape="doublecircle")
            else:
                g.node(e)
            if e in inicio:
                g.edge('ini',e)
        for t in trans:
            if t[2] not in alfabeto:
                return 0
            g.edge(str(t[0]), str(t[1]), label=str(t[2]))
        g.render(view=True)


    
dawg = Dawg()
palabraCount = 0
palabras = open(DICTIONARY, "rt").read().split()
palabras.sort()


start = time.time()    
for palabra in palabras:
    palabraCount += 1
    dawg.insert(palabra)
    
#dawg.display()
dawg.finish()
print("Tiempo de creacion: {0} s".format(time.time()-start))
dawg.display()
cantidadAristas = dawg.aristasCount()
print("Palabras {0}, nodos {1}".format(palabraCount, dawg.nodosCount()+1))
