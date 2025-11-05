class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2
    
    def left(self, i):
        return 2*i + 1
    
    def right(self, i):
        return 2*i + 2

    #Reajusta hacia arriba: si el hijo es menor que el padre
    def heapifyUp(self, i):
        while i != 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def swap(self, i, j):
        temp = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = temp

    #Reajusta hacia abajo: si alguno de los hijos es menor
    def heapifyDown(self, i):
        size = len(self.heap)
        smallest = i
        l = self.left(i)
        r = self.right(i)

        if (l < size and self.heap[l] < self.heap[smallest]):
            smallest = l
        if (r < size and self.heap[r] < self.heap[smallest]):
            smallest = r

        if (smallest != i):
            self.swap(i, smallest)
            self.heapifyDown(smallest)
    
    def buildHeap(self, input):
        self.heap = list(input)
        size = len(self.heap)
        inicio = self.parent(size-1)
        
        for i in range(inicio, -1, -1):
            self.heapifyDown(i)

    #Insertar elemento y mantener propiedad del heap mínimo
    def insert(self, key):
        self.heap.append(key)
        self.heapifyUp(len(self.heap)-1)


    #Eliminar una clave específica
    def deleteKey(self, key):

        index = -1
        size = len(self.heap)

        for i in range(size):
            if self.heap[i] == key:
                index = i
                break
        if index == -1:
            print(f"No se  halló la llave {key} en el heap")
            return
        
        ultimo = self.heap.pop()

        if index == len(self.heap):
            return
        
        self.heap[index] = ultimo

        self.valor = self.heap[index]
        parentvalor = self.heap[self.parent(index)]

        if index > 0 and self.valor < parentvalor:
            self.heapifyUp(index)
        else:
            self.heapifyDown(index)

    def printHeap(self):
        for valor in self.heap:
            print(valor, end=" ")
        print("")

# -------- Main function --------
if __name__ == "__main__":

    heap = MinHeap()

    input = [40, 20, 15, 30, 10]
    heap.buildHeap(input)

    print("Heap mínimo construido a partir de la lista: ", end=" ")
    heap.printHeap()

    heap.insert(5)
    print("Después de insertar el 5: ", end=" ")
    heap.printHeap()

    heap.deleteKey(15)
    print("Después de borrar el 15: ", end=" ")
    heap.printHeap()

    heap.deleteKey(30)
    print("Después de borrar el 30: ", end=" ")
    heap.printHeap()