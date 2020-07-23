import sys
import time

DICTIONARY = "DICTIONARY.txt"
QUERY = sys.argv[1:]

# Esta clase representa un nodo en el gráfico de palabras acíclicas dirigido (DAWG).
# Tiene una lista de aristas a otros nodos. Tiene funciones para probar si es equivalente a otro nodo.
# Los nodos son equivalentes si tienen bordes idénticos, y cada borde idéntico conduce a estados idénticos.
# Las funciones __hash__ y __eq__ permiten que se use como clave en un diccionario de Python.

class DawgNode:
    NextId = 0
    
    def __init__(self):
        self.id = DawgNode.NextId
        DawgNode.NextId += 1
        self.final = False
        self.edges = {}

        # Número de nodos finales accesibles desde este.
        self.count = 0

    def __str__(self):        
        arr = []
        if self.final: 
            arr.append("1")
        else:
            arr.append("0")

        for (label, node) in self.edges.items():
            arr.append( label )
            arr.append( str( node.id ) )

        return "_".join(arr)

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def numReachable(self):
        # si ya se ha asignado un recuento, devuélvalo
        if self.count: 
            return self.count

        # cuenta el número de nodos finales a los que se puede acceder desde este.
        # incluido uno mismo
        count = 0
        if self.final: 
            count += 1
        for label, node in self.edges.items():
            count += node.numReachable()

        self.count = count
        return count

class Dawg:
    def __init__(self):
        self.previousWord = ""
        self.root = DawgNode()
        # Aquí hay una lista de nodos que no han sido verificados por duplicacion.
        self.uncheckedNodes = []
        # Aquí hay una lista de nodos únicos que han sido verificados por duplicación.
        self.minimizedNodes = {}
        # Aquí están los datos asociados con todos los nodos
        self.data = []

    def insert( self, word, data ):
        if word <= self.previousWord:
            raise Exception("Error: Las palabras deben insertarse en orden alfabetico " +
                "orden.")

        # encuentra el prefijo común entre la palabra y la palabra anterior
        commonPrefix = 0
        for i in range( min( len( word ), len( self.previousWord ) ) ):
            if word[i] != self.previousWord[i]: break
            commonPrefix += 1

        # Compruebe los uncheckedNodes para los nodos redundantes, que procede del último hasta el tamaño prefijo común.
        # Luego truncar la lista en ese punto.
        self._minimize( commonPrefix )

        self.data.append(data)
        # agregue el sufijo, comenzando desde el nodo correcto a la mitad del gráfico
        if len(self.uncheckedNodes) == 0:
            node = self.root
        else:
            node = self.uncheckedNodes[-1][2]

        for letter in word[commonPrefix:]:
            nextNode = DawgNode()
            node.edges[letter] = nextNode
            self.uncheckedNodes.append( (node, letter, nextNode) )
            node = nextNode

        node.final = True
        self.previousWord = word

    def finish( self ):
        # Minimizar todas uncheckedNodes
        self._minimize( 0 );
        # revisa toda la estructura y asigna los recuentos a cada nodo.
        self.root.numReachable()

    def _minimize( self, downTo ):
        # proceder desde la hoja hasta cierto punto
        for i in range( len(self.uncheckedNodes) - 1, downTo - 1, -1 ):
            (parent, letter, child) = self.uncheckedNodes[i];
            if child in self.minimizedNodes:
                # reemplazar el niño con el encontrado anteriormente
                parent.edges[letter] = self.minimizedNodes[child]
            else:
                # agrega el estado a los nodos minimizados.
                self.minimizedNodes[child] = child;
            self.uncheckedNodes.pop()

    def lookup( self, word ):
        node = self.root
        skipped = 0 # realizar un seguimiento de la cantidad de nodos finales que omitimos
        for letter in word:
            if letter not in node.edges: return None
            for label, child in sorted(node.edges.items()):
                if label == letter: 
                    if node.final: skipped += 1
                    node = child
                    break
                skipped += child.count

        if node.final:
            return self.data[skipped]

    def nodeCount( self ):
        return len(self.minimizedNodes)

    def edgeCount( self ):
        count = 0
        for node in self.minimizedNodes:
            count += len(node.edges)
        return count

    def display(self):
        stack = [self.root]
        done = set()
        while stack:
            node = stack.pop()
            if node.id in done: continue
            done.add(node.id)
            print("{}: ({})".format(node.id, node))
            for label, child in node.edges.items():
                print("    {} goto {}".format(label, child.id))
                stack.append(child)

if 0:
    dawg = Dawg()
    dawg.insert("cat", 0)
    dawg.insert("catnip", 1)
    dawg.insert("zcatnip", 2)
    dawg.finish()
    dawg.display()
    sys.exit()
            
dawg = Dawg()
WordCount = 0
words = open(DICTIONARY, "rt").read().split()
words.sort()
start = time.time()    
for word in words:
    WordCount += 1
    # inserte todas las palabras, utilizando la versión invertida como los datos asociados a ella
    dawg.insert(word, ''.join(reversed(word)))
    if ( WordCount % 100 ) == 0: 
        print("{0}\r".format(WordCount), end="")


dawg.finish()
print("Tiempo de creacion de Dawg {0} s".format(time.time()-start))

EdgeCount = dawg.edgeCount()
print("Leer {0} palabras en {1} nodos y {2} arista".format(
    WordCount, dawg.nodeCount(), EdgeCount))

print("Esto podría almacenarse en tan poco como {0} bytes".format(EdgeCount * 4))

for word in QUERY:
    result = dawg.lookup(word)
    if result == None:
        print("{0} no en el diccionario.".format(word))
    else:
        print("{0} está en el diccionario y tiene datos {1}".format(word, result))
