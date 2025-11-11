import algoritmoWPGMA
import ConstruirMatriz

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

wpgma = algoritmoWPGMA.WPGMA(matriz)
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