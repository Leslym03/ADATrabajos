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
        # dict => map
        self.aristas = {}
        self.altura = 0
        # Número de nodos finales accesibles desde este.
        self.count = 0

        # final o no final
    def __str__(self):        
        arr = []
        if self.final: 
            arr.append("1")
        else:
            arr.append("0")

        # Devuelve una lista de tuplas, cada tupla se compone de dos elementos: 
        # el primero será la clave y el segundo, su valor.
        for (etiqueta, node) in self.aristas.items():
            arr.append( etiqueta )       # a,b,c,
            arr.append( str( node.id ) ) # 1,2,3 ->id

        return "_".join(arr)

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    # cuente el número de nodos finales que son accesibles desde este, 
    # incluido el propio
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
        self.nodosMinimizados = {} # es como un map
        #self.data = []

    def insert( self, palabra ):
        #eliminar
        if palabra <= self.palAnterior:
            raise Exception("Error: Las palabras deben insertarse en orden alfabetico " +
                "orden.")

        prefijoComun = 0

        #insercion ordenada por prefijos de la palabra original
        # coje coa y coc
        for i in range( min( len( palabra ), len( self.palAnterior ) ) ):
            if palabra[i] != self.palAnterior[i]: 
                break
            prefijoComun += 1

        self._minimizar( prefijoComun )

        #self.data.append(data)

        # a== raiz
        # c== raiz
        if len(self.noVerificados) == 0:
            node = self.root
        else:
            # [0,0,0]
            # cocoa : ultimo en la lista = [0,0,posicion del 2]
            # [[0_o_3,o,3]
            node = self.noVerificados[-1][2] # node = 3



        # fruta = "banana"
        # fruta[2:] 'nana'
        # sufijo de palabra


        # a[0:] -> recorre toda palabra  
        # coa[0:] -> recorre toda la palabra
        # cocoa[2:] -> coa
        for letra in palabra[prefijoComun:]:
            # crea nodos y le asigna la letra como arista
            # agrega los nodos a la cola de no verificados
            nextNode = Estado()
            # nod. aristas clave = valor
            node.aristas[letra] = nextNode
            # noVerificados[nodo, letra, nextnodo]
            # [0_a_1][a][0]
            self.noVerificados.append( (node, letra, nextNode) )
            print(node.id)
            print(letra)
            print(nextNode.id)
            node = nextNode

        # noverfi -> a -> [0_a_1, a, 1]
        # noverfi -> coa -> [0_a_1_c_2,c,2], [0_o_3,o,3], [0_a_4,a,4]
        # noverfi -> cocoa -> [0_a_1_c_5], [0_o_6], [0_a_7]


        node.final = True       # pone la letra como nodo final 
        self.palAnterior = palabra  # palabra se vuelve palabra anterior 

    def finish( self ):
        # se intercambio para que parezaca revuz :v
        #intercambiar al final
        self._minimizar( 0 );
        self.root.numAccesible()
        

    # minimiza como pila de noverificados

    def _minimizar( self, downTo ):

        # for (i=-1; i hasta -1; i--) --> a
        # for (i=0; i hasta -1; i-- ) ->  a,coa: finish
        # for (i=2; i hasta 1; i--) ->> a, coa, cocoa
        # for (i=4; i hasta 0; i--) -> minifinish
        for i in range( len(self.noVerificados) - 1, downTo - 1, -1 ):
            # [padre][letra][hijo] = apunta al ultimo elemento nextNode
            # [0_a_4,a,4] =>    i =2
            (padre, letra, hijo ) = self.noVerificados[i];
            if hijo in self.nodosMinimizados:
                padre.aristas[letra] = self.nodosMinimizados[hijo]
            else:
                self.nodosMinimizados[hijo] = hijo;
            # nodosMinimizados{nodeNex: nodeNex} => a, 1
            # coa-> 4
            self.noVerificados.pop()
            # noverfi -> coa -> [0_a_1_c_2,c,2], [0_o_3,o,3]

    #def buscar( self, palabra ):
        #node = self.root
        #omitido = 0 
        #for letra in palabra:
            #if letra not in node.aristas: 
                #return None
            #for etiqueta, hijo in sorted(node.aristas.items()):
                #if etiqueta == letra: 
                    #if node.final: 
                        #omitido += 1
                    #node = hijo
                    #break
                #omitido += hijo.count

        #if node.final:
            #return self.data[omitido]

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
