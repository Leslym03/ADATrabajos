import sys
import time

DICTIONARY = "DICTIONARY.txt"
QUERY = sys.argv[1:]

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
        for i in range( min( len( palabra ), len( self.palAnterior ) ) ):
            if palabra[i] != self.palAnterior[i]: break
            prefijoComun += 1

        self._minimizar( prefijoComun )

        self.data.append(data)

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

    def buscar( self, palabra ):
        node = self.root
        omitido = 0 
        for letra in palabra:
            if letra not in node.aristas: return None
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

    def display(self):
        stack = [self.root]
        done = set()
        while stack:
            node = stack.pop()
            if node.id in done: 
                continue
            done.add(node.id)
            print("{}: ({})".format(node.id, node))
            for etiqueta, hijo in node.aristas.items():
                print("    {} - {}".format(etiqueta, hijo.id))
                stack.append(hijo)


            
dawg = Dawg()
palabraCount = 0
palabras = open(DICTIONARY, "rt").read().split()
palabras.sort()


start = time.time()    
for palabra in palabras:
    palabraCount += 1
    dawg.insert(palabra, ''.join(reversed(palabra)))
    

dawg.finish()
print("Tiempo de creacion: {0} s".format(time.time()-start))

cantidadAristas = dawg.aristasCount()
print("Palabras {0}, nodos {1}, aristas {2}".format(
    palabraCount, dawg.nodosCount(), cantidadAristas))
