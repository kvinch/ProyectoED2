import ConstruirMatriz
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

        for etiqueta in etiquetas:
            nodo = NodoCluster(etiqueta = etiqueta)
            self.cluster.append(nodo)
            self.altura.insertar(nodo, 0.0) #Se crea un nodo para cada etiqueta: {"A":0.0, "B":0.0", "C":0.0} -> Es un HashTable
        
        


    def distanciaMin(self): #Encontramos los índices con menor valor dentro de la matriz
        minimo = 99999 #Un número muy grande
        min_i = -1
        min_j = -1

        for i in range(self.n):
            for j in range(i+1,self.n): #Se le suma un +1 para evitar correr desde el 0.0, porque sino detectaría como el menor, porque es simétrica
                if self.matriz[i][j] < minimo:
                    minimo = self.matriz[i][j] #Se actualiza el nuevo valor
                    min_i = i
                    min_j = j            
        return sorted((min_i, min_j)) #Retorna los índices de manera ordenada
    
    def retornarNewick(self, NodoCluster):
        if NodoCluster.izq is None and NodoCluster.der is None:
            return f"{NodoCluster.etiqueta}:{NodoCluster.distancia}"
        else:
            izq = self.retornarNewick(NodoCluster.izq)
            der = self.retornarNewick(NodoCluster.der)
            return f"({izq},{der}):{NodoCluster.distancia}"

    def wpgma(self):
        while(self.n>1):
            x,y = self.distanciaMin() #Se encuentran los índices para el menor valor
            menorDistancia = self.matriz[x][y]
            #Se crea un nuevo cluster y se agrega a la
            nodoX = self.cluster[x]
            nodoY = self.cluster[y]

            alturaX = self.altura.get(nodoX)
            alturaY = self.altura.get(nodoY)
            nodoX.distancia = menorDistancia/2 - alturaX
            nodoY.distancia = menorDistancia/2 - alturaY
            

            nuevoCluster = NodoCluster(izq = nodoX, der = nodoY)
            self.cluster.append(nuevoCluster)
            self.altura.insertar(nuevoCluster, menorDistancia/2)

            #Calculamos las distancias de los diferentes valores 
            DistanciasValores  = []
            for i in range(len(self.cluster)-1):
                if i not in (x,y):
                    distancia = (self.matriz[x][i] + self.matriz[y][i])/2 #Se calculan las distancias, por ejemplo: (d(A,B) + d(A,D))/2 = d(A,(BD))  
                    DistanciasValores.append(distancia)

            #Actualizamos todos los valores con la lista de valores
            nuevaMatriz = [] #Se crea una matriz nueva
            #Construimos la cantidad de índices necesarios
            indices = []
            for g in range(self.n): 
                if g not in (x,y): #No se agregan estos, porque terminaran juntándose
                    indices.append(g)

            for c in indices: #Iteramos por toda la cantidad de índices
                fila = [] #Creamos una fila nueva, donde vamos a añadirla a la matriz nueva
                for a in indices:
                    fila.append(self.matriz[c][a]) #Agregamos todos los valores de la matriz anterior
                nuevaMatriz.append(fila) 


            for indice, valor in enumerate(DistanciasValores): #Se agregan las 
                nuevaMatriz[indice].append(valor)

            nuevaMatriz.append(list(DistanciasValores) + [0.0])
            del DistanciasValores

            self.matriz = nuevaMatriz #Actualizamos para la nueva matriz
            self.n = len(nuevaMatriz) #Actualizamos el largo de la matriz


            del self.cluster[y]
            del self.cluster[x] #Eliminamos los cluster antiguos
            
            Nodo = self.cluster[0]


        return f"({self.retornarNewick(Nodo.izq)},{self.retornarNewick(Nodo.der)});"

otus = [
        "ATCG",
        "ATGG",
        "TTGG",
        "TCGG"
    ]

matriz = ConstruirMatriz.construirMatriz(otus)


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


wpgma = WPGMA(distancia_matriz)
a = wpgma.wpgma() 
print(a)





