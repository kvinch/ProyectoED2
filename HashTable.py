#Código adaptado de Clase de HashTables a Python

class Hash():

    def __init__(self, n):
        self.n = n
        self.bins = [[] for i in range(self.n)] #Chaining por si existen colisiones
    
    def FuncionHash(self, clave):
        clave = str(id(clave))
        h = 0
        for letra in clave:
            h = (h * 31 + ord(letra)) % self.n
        return h
    
    def insertar(self, clave, nuevo_valor):
        indice = self.FuncionHash(clave)
        lista = self.bins[indice]

        for i, (key,valor) in enumerate(lista):
            if clave is key: #Significa que es duplicado y ya existe 
                lista[i] = (clave,valor) #Remplazamos con los datos que nos dieron
                return None
        
        lista.append((clave,nuevo_valor)) #Agregamos a la lista si es que está vacia

    
    def get(self, clave): #Devolver el valor
        indice = self.FuncionHash(clave)
        lista = self.bins[indice]

        for key, valor in lista: 
            if clave is key:  #Si es igual
                return valor
            
        return 0.0
    

