import ConstruirMatriz
import string

class WPGMA:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.etiquetas = list(string.ascii_uppercase[:self.n]) #Se sacan las etiquetas del abecedario hasta la letra del tamaño de la matriz
        self.cluster = [cluster for cluster in self.etiquetas] #Se crean los clusters a partir de las etiquetas: ["A", "B", "C", "D"...]
        self.altura = {etiqueta:0.0 for etiqueta in self.etiquetas} #Se crea un valor para cada etiqueta: {"A":0.0, "B":0.0", "C":0.0} -> Es un diccionario

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
    
    def wpgma(self):
        while(self.n>1):
            x,y = self.distanciaMin() #Se encuentran los índices para el menor valor
            menorDistancia = self.matriz[x][y]
            #Se crea un nuevo cluster y se agrega a la
            nuevaCluster = f"({self.cluster[x]}:{menorDistancia/2-self.altura[self.cluster[x]]},{self.cluster[y]}:{menorDistancia/2-self.altura[self.cluster[y]]})" 
            print(f"La altura x: {menorDistancia/2-self.altura[self.cluster[x]]}")
            print(f"La altura y: {menorDistancia/2-self.altura[self.cluster[y]]}")
            self.cluster.append(nuevaCluster)
            #Calculamos las distancias de los diferentes valores 
            DistanciasValores  = []
            for i in range(len(self.cluster)-1):
                if i not in (x,y):
                    distancia = (self.matriz[x][i] + self.matriz[y][i])/2 #Se calculan las distancias, por ejemplo: (d(A,B) + d(A,D))/2 = d(A,(BD))  
                    DistanciasValores.append(distancia)

            alturaCluster = menorDistancia/2
            self.altura[nuevaCluster] = alturaCluster


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
    
            #ConstruirMatriz.imprimirMatriz(nuevaMatriz)
            self.matriz = nuevaMatriz #Actualizamos para la nueva matriz
            self.n = len(nuevaMatriz) #Actualizamos el largo de la matriz

            del self.cluster[y]
            del self.cluster[x] #Eliminamos los clusters antiguos
            

        return self.cluster[0]

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
wpgma = WPGMA(matrix)
a = wpgma.wpgma() + ";"
print(a)


