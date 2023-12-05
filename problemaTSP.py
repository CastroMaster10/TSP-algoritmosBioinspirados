from sys import maxsize 
from itertools import permutations

def travellingSalesmanProblem(graph,V): 

    vertex = [i for i in range(V)]  # Lista de todos los nodos

    min_path = maxsize 
    min_permutation = None
    next_permutation = permutations(vertex)
    for i in next_permutation:
        current_pathweight = 0
        k = i[0]  # El primer nodo es el primer elemento de la permutación
        for j in i[1:]: 
            current_pathweight += graph[k][j] 
            k = j 
        current_pathweight += graph[k][i[0]]  # Regresar al primer nodo

        if current_pathweight < min_path:
            min_path = current_pathweight
            min_permutation = i

    # Añadir el primer nodo al final del camino para completar el ciclo
    min_permutation = min_permutation + (min_permutation[0],)

    return min_path, min_permutation

