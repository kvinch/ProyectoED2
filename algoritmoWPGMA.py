import ConstruirMatriz
import MinHeap
import HashTable
import string

class NodoCluster:

    def __init__(self, etiqueta = None, izq = None, der = None, distancia = 0.0):
        self.etiqueta = etiqueta
        self.izq = izq
        self.der = der
        self.distancia = distancia

class WPGMA:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        etiquetas = list(string.ascii_uppercase[:self.n])
        #Se crean los clusters a partir de las etiquetas: ["A", "B", "C", "D"...]
        self.cluster = []
        self.altura = HashTable.Hash(n = self.n * 2 - 1) #-> La cantidad máxima de clusters que se pueden generar son 2n -1

        self.cluster_activo = self.n * [True] #Lista de booleano para identificar clusters aun no agrupados
        self.num_activos = self.n #Contador clusters no agrupados


        for etiqueta in etiquetas:
            nodo = NodoCluster(etiqueta = etiqueta)
            self.cluster.append(nodo)
            self.altura.insertar(nodo, 0.0) #Se crea un nodo para cada etiqueta: {"A":0.0, "B":0.0", "C":0.0} -> Es un HashTable

        self.heap = MinHeap.MinHeap()
        for i in range(self.n):
            for j in range(i+1, self.n):
                dist = self.matriz[i][j]
                tupla = (dist,i,j)
                self.heap.insert(tupla)

    def distanciaMin2(self): #Encontramos los índices con menor valor dentro de la matriz usando MinHeap
        while True:
            valorM = self.heap.extraerMin()
            if valorM == -1: break #si heap vacio, terminar
            (dist,i,j) = valorM

            if self.cluster_activo[i] and self.cluster_activo[j]: #comprobar si ambos clusters no fueron agrupados
                return sorted((i,j))
        return -1, -1
    
    def distanciaMin(self): #Encontramos los índices con menor valor dentro de la matriz usando MinHeap
        while True:
            valorM = self.heap.extraerMin()
            if valorM == -1: break #si heap vacio, terminar
            (dist,i,j) = valorM #Agrupamos el valor

            if self.cluster_activo[i] and self.cluster_activo[j]: #comprobar si ambos clusters no fueron agrupados
                dist_actual = self.matriz[min(i, j)][max(i, j)] #Se busca el valor actual de la matriz original

                if abs(dist - dist_actual) <= 0.0001: #Verificamos que sean iguales, al ser flotantes, entonces existen la posibilidad de que tengan una diferencia leve
                    return sorted((i, j))
        return -1, -1

    def retornarNewick(self, NodoCluster):
        if NodoCluster.izq is None and NodoCluster.der is None:
            return f"{NodoCluster.etiqueta}:{NodoCluster.distancia}"
        else:
            izq = self.retornarNewick(NodoCluster.izq)
            der = self.retornarNewick(NodoCluster.der)
            return f"({izq},{der}):{NodoCluster.distancia}"

    def wpgma(self):
        while(self.num_activos>1):
            x,y = self.distanciaMin() #Se encuentran los índices para el menor valor
            if x == -1:
                break

            menorDistancia = self.matriz[x][y]
            #Se crea un nuevo cluster y se agregan sus hijos
            nodoX = self.cluster[x]
            nodoY = self.cluster[y]

            alturaX = self.altura.get(nodoX)
            alturaY = self.altura.get(nodoY)
            nodoX.distancia = menorDistancia/2 - alturaX #Se actualiza la distancia con la fórmula de WPGMA: 
            nodoY.distancia = menorDistancia/2 - alturaY
            

            nuevoCluster = NodoCluster(izq = nodoX, der = nodoY)
            self.cluster[x] = nuevoCluster #Sobreescribir nuevo cluster que representa el nuevo agrupado 
            self.altura.insertar(nuevoCluster, menorDistancia/2)

            for i in range(self.n):
                if i==x or i==y or not self.cluster_activo[i]:
                    continue

                #Ahora tenemos que calcular las distancias del nuevo cluster a los demas
                dist_xi = self.matriz[min(x,i)][max(x,i)] #Leemos distancias desde la matriz
                dist_yi = self.matriz[min(y,i)][max(y,i)] #Usamos min y max porque debemos asegurarnos de usar los indices actualizados

                nueva_distancia = (dist_xi + dist_yi)/2
                self.matriz[min(x,i)][max(x,i)] = nueva_distancia #actualizamos la matriz en la nueva posicion

                self.heap.insert((nueva_distancia,min(x,i),max(x,i)))

            self.cluster_activo[y] = False #al cluster lo marcamos como inactivo
            self.num_activos -= 1 #Un cluster activo menos

            final_ind = -1
            #Encontrar único true
            for i in range(len(self.cluster_activo)):
                if self.cluster_activo[i] == True:
                    final_ind = i
                    break

            if final_ind == -1:
                return "No se encontró cluster final"   

        Nodo = self.cluster[final_ind]
        
        if Nodo.izq is not None and Nodo.der is not None: #Si tiene hijos, entonces retorna el izq y  derecho
            return f"({self.retornarNewick(Nodo.izq)},{self.retornarNewick(Nodo.der)});"
        else:
            return f"{self.retornarNewick(Nodo)};"

otus = [
    "ATCGATCGATCGAT",
    "ATCGATCGATCGAA",
    "ATCGATCGATCAAA",
    "ATCGATCGAACAAA",
    "TACGTACGTACGTC",
    "CATGTACGTACGTA"
]

matriz = ConstruirMatriz.construirMatriz(otus)
ConstruirMatriz.imprimirMatriz(matriz)


matrix =[
    
 [1,    0.82, 0.69, 0.78, 0.73],
 [0.82, 1,    0.78, 0.92, 0.80],
 [0.69, 0.78, 1,    0.80, 0.86],
 [0.78, 0.92, 0.80, 1,    0.75],
 [0.73, 0.80, 0.86, 0.75, 1]

]

distancia_matriz = [
    [0.0, 0.2, 0.8, 0.9],
    [0.2, 0.0, 0.7, 0.8],
    [0.8, 0.7, 0.0, 0.3],
    [0.9, 0.8, 0.3, 0.0]
]

mat = [
	[0,17,	21,	31,	23],
	[17,	0,	30,	34,	21],
	[21,	30,	0,	28,	39]	,
    [31,	34,	28,	0,	43],
	[23,	21,	39,	43,	0]
    ]

wpgma = WPGMA(mat)
a = wpgma.wpgma() 
print(a)

try:  #Intentamos importar las librerías necesarioas para la visualización
	import io
	from Bio import Phylo
	import matplotlib.pyplot as plt
	newick = io.StringIO(a)
	tree = Phylo.read(newick, "newick")
	fig = plt.figure(figsize=(10, 6), dpi=100)
	axes = fig.add_subplot(1, 1, 1)
	Phylo.draw(tree, axes=axes)
	plt.show() #Muestra el gráfico en una ventana aparte
except ImportError:  #Las librerías no están instaladas
	print("No se puede visualizar, porque las librerías no están instaladas")








