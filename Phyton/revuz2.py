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


    def numAccesible(self):
        if self.count: 
            return self.count

        count = 0
        if self.final: 
            count += 1
        # Devuelve una lista de tuplas, cada tupla se compone de dos elementos: 
        # el primero será la clave y el segundo, su valor.
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
        self.data = []

    def insert( self, palabra, data ):
        if palabra <= self.palAnterior:
            raise Exception("Error: Las palabras deben insertarse en orden alfabetico " +
                "orden.")

        prefijoComun = 0

        #insercion ordenada por sufijos de la palabra original (prefijos reverso)
        for i in range( min( len( palabra ), len( self.palAnterior ) ) ):
            if palabra[i] != self.palAnterior[i]: 
                break
            prefijoComun += 1

        self._minimizar( prefijoComun )

        self.data.append(data)

        # a== raiz
        if len(self.noVerificados) == 0:
            node = self.root
        else:
            # [0,0,0]
            # cola : ultimo en la lista = [0,0,posicion del 2]
            node = self.noVerificados[-1][2] # a-> 0
            # [0, a, 1]
            # coa ->  node = 1





        # fruta = "banana"
        # fruta[3:] 'ana'
        # sufijo de palabra


        # coa[0:] -> vacio
        for letra in palabra[prefijoComun:]:
            # crea nodos y le asigna la letra como arista
            # agrega los nodos a la cola de no verificados
            nextNode = Estado()
            node.aristas[letra] = nextNode
            # noVerificados[nodo, letra, nextnodo]
            self.noVerificados.append( (node, letra, nextNode) )
            node = nextNode



        # noverfi -> a -> [0, a, 1]
        # noverfi -> coa -> [1,c,2], [2,o,3], [3,a,4]





        node.final = True       # pone la letra como nodo final 
        self.palAnterior = palabra  # palabra se vuelve palabra anterior 

    def finish( self ):

        self._minimizar( 0 );
        self.root.numAccesible()

    def _minimizar( self, downTo ):

        # for (i=-1; i<-1; i--) --> a
        for i in range( len(self.noVerificados) - 1, downTo - 1, -1 ):
            (padre, letra, hijo ) = self.noVerificados[i];
            if hijo in self.nodosMinimizados:
                padre.aristas[letra] = self.nodosMinimizados[hijo]
            else:
                self.nodosMinimizados[hijo] = hijo;
            self.noVerificados.pop()

    def buscar( self, palabra ):
        node = self.root
        omitido = 0 
        for letra in palabra:
            if letra not in node.aristas: 
                return None
            for etiqueta, hijo in sorted(node.aristas.items()):
                if etiqueta == letra: 
                    if node.final: 
                        omitido += 1
                    node = hijo
                    break
                omitido += hijo.count

        if node.final:
            return self.data[omitido]

    def nodosCount( self ):
        return len(self.nodosMinimizados)

    def aristasCount( self ):
        count = 0
        for node in self.nodosMinimizados:
            count += len(node.aristas)
        return count

    def draw(self,alfabeto, estados, inicio, trans, final):
        print("inicio:", str(inicio))
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
            
dawg = Dawg()
palabraCount = 0
palabras = open(DICTIONARY, "rt").read().split()
palabras.sort()


start = time.time()    
for palabra in palabras:
    palabraCount += 1
    dawg.insert(palabra, ''.join(reversed(palabra)))#reversa de palabra
    

dawg.finish()

print("Tiempo de creacion: {0} s".format(time.time()-start))
dawg.display()
cantidadAristas = dawg.aristasCount()
print("Palabras {0}, nodos {1}".format(palabraCount, dawg.nodosCount()+1))



