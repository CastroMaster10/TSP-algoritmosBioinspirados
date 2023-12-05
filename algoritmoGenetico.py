import random
import timeit
import csv
import math

def generar_poblacion_inicial(n_individuos, numeroNodos):
    poblacion = []
    for i in range(n_individuos):
        n_nodos = [i for i in range(numeroNodos)] #guardamos el numero de nodos a utilizar
        elementosUnicos = numeroNodos
        individuo = random.sample(n_nodos,elementosUnicos)
        primerElemento = individuo[0]
        individuo.append(primerElemento) #se devuelve a donde mismo
        individuo_str = '->'.join(map(str, individuo))
        poblacion.append(individuo_str)
    
    
    return poblacion

#fitness_individuo =  sum(int(bit)*peso for bit, peso in zip(individuo, beneficios))
#ordenar poblacion en base a poblacion fitness
def ordenar_poblacion(poblacion):
    return {k: v for k, v in sorted(poblacion.items(), key=lambda item: item[1],reverse=True)}

def evaluar_factibilidad(individuo):

    valido = True #Variable para saber si una tarea es valida

    individuo_lista = list(map(int,individuo.split("->")))
    conjunto =  set(individuo_lista)

    if len(individuo_lista) - 1 > len(conjunto):
        valido = False


    
    return valido


#evaluar funcionFitness
def evaluarFuncionFitness(individuos,matrizDistancias,numeroNodos):
    poblacion = {}
    for individuo in individuos:
        individuo_list  = list(map(int,individuo.split("->"))) #Convertimos los valores a una lista
        f_o = 0 #distancia recorrida
        for i in range(numeroNodos):
            try:
                nodo_i = individuo_list[i]
                nodo_j = individuo_list[i+1]
                f_o += matrizDistancias[nodo_i][nodo_j]
            except:
                continue
        
        poblacion[individuo] = f_o #distancia recorrida

    return ordenar_poblacion(poblacion)  #ordenar en funcion al valor funcion fitness


def cruce_ordenado(padre1, padre2):
    # Seleccionar un subconjunto aleatorio del primer padre
    tamaño = len(padre1)
    inicio, fin = sorted(random.sample(range(tamaño), 2))

    # Mantener los elementos del primer padre en las posiciones seleccionadas
    hijo = [None]*tamaño
    hijo[inicio:fin] = padre1[inicio:fin]

    # Rellenar las posiciones restantes con los elementos del segundo padre en su orden original
    for elemento in padre2:
        if elemento not in hijo:
            for i in range(tamaño):
                if hijo[i] is None:
                    hijo[i] = elemento
                    break
    
    # Verificar si quedó algún espacio vacío y rellenarlo
    for i in range(tamaño):
        if hijo[i] is None:
            for elemento in padre2:
                if elemento not in hijo:
                    hijo[i] = elemento
                    break

    hijo[-1] = hijo[0]
    return hijo

def cruce_ordenado_doble(padre1, padre2):
    hijo1 = cruce_ordenado(padre1, padre2)
    hijo2 = cruce_ordenado(padre2, padre1)
    return hijo1, hijo2

def mutacion(individuo):
    # Seleccionar dos índices aleatorios
    tamaño = len(individuo)
    idx1, idx2 = random.sample(range(tamaño), 2)

    # Intercambiar los elementos en los índices seleccionados
    individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]

    return individuo


def algoritmoGenetico_TSP(poblacion,matrizDistancias,generaciones,numeroNodos,factibilidad=True):

    p_cruce = 0.9 #probabilidad de cruce
    p_mutacion = 0.3 #probabilidad de mutacion

    #Iteramos sobre las generaciones
    for n in range(generaciones):

        #Generamos probabilidad de cruce
        cruce = random.random()
        if cruce < p_cruce:
            individuos = list(poblacion.keys())
            numero_padre1,numero_padre2 = random.sample(range(0, len(individuos)), 2) #numero de padre

            padre1 = list(map(int,individuos[numero_padre1].split("->"))) 
            padre2 =  list(map(int,individuos[numero_padre2].split("->")))

            hijo1,hijo2 = cruce_ordenado_doble(padre1,padre2)


            #mutacion de cada hijo
            mutacionProbabilidad = random.random()
            if mutacionProbabilidad < p_mutacion:
                hijo1 = mutacion(hijo1)
                hijo2 = mutacion(hijo2)
            
            
            #Si queremos factibilidad checamos si el individuo cumple con ella
            hijo1 = '->'.join(map(str, hijo1))
            hijo2 = '->'.join(map(str, hijo2))
            nuevosIntegrantes = [hijo1,hijo2]
            integrantes_filtrados = []
            if factibilidad:
                for hijo in nuevosIntegrantes:
                    factible = evaluar_factibilidad(hijo)
                    if factible == True and (hijo not in individuos):
                        integrantes_filtrados.append(hijo)

            if integrantes_filtrados:
                #print("Integrantes filtrados: ",integrantes_filtrados)
                subPoblacion = evaluarFuncionFitness(nuevosIntegrantes,matrizDistancias,numeroNodos)
                poblacion_original_debiles = dict(list(poblacion.items())[:2])

                # Unimos los dos diccionarios
                poblacionMerge = {**subPoblacion, **poblacion_original_debiles}

                # Ordenamos el diccionario total por valor de forma ascendente
                poblacionMerge = dict(sorted(poblacionMerge.items(), key=lambda item: item[1]))
                # Creamos un nuevo diccionario con los dos primeros elementos del diccionario ordenado
                nuevaSubPoblacion = dict(list(poblacionMerge.items())[:2])

                nuevaSubPoblacion_ordenada = ordenar_poblacion(nuevaSubPoblacion)

                #Eliminamos los antiguos individuos y agregamos los nuevos
                oldIndividuals = individuos[:2]
                del poblacion[oldIndividuals[0]]
                del poblacion[oldIndividuals[1]]

                for newIndividual,fitness in nuevaSubPoblacion_ordenada.items():
                    poblacion[newIndividual] = fitness

                poblacion = ordenar_poblacion(poblacion)

    return poblacion


# Open the CSV file
with open('matrizDistancias/150 nodos/matrizDistancia1.csv', 'r') as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader)
    # Convert the CSV reader to a list of lists and convert each value to an integer
    graph = [[float(value) for value in row] for row in reader]
    graph = [row[1:] for row in graph]

# Now, 'graph' is a list of lists representing your CSV file
#print(graph)
#print()

numeroNodos = 150
start_time = timeit.default_timer()
generacion_individuos = generar_poblacion_inicial(100,numeroNodos) #poblacion inicial con factibilidad
poblacion_inicial =  evaluarFuncionFitness(generacion_individuos,graph,numeroNodos)

print(poblacion_inicial)
print()

poblacion_final = algoritmoGenetico_TSP(poblacion_inicial,graph,6000,numeroNodos,factibilidad=True)
end_time = timeit.default_timer()
execution_time =  end_time - start_time
print(poblacion_final)
print("Tiempo de ejecucion: ",execution_time)



"""
individuo =  '2->9->31->17->1->0->19->5->7->10->20->35->14->25->13->23->37->32->18->39->16->29->33->21->15->26->3->34->22->38->11->24->8->6->30->28->12->4->27->2'
individuo_lista = list(map(int,individuo.split("->"))) 
print(set(sorted(individuo_lista)))
print(len(individuo_lista) - 1)
print(len(set(individuo_lista)))

numeroNodos = 40
corte1 = math.ceil(numeroNodos / 2)
individuo_str1 = '13->39->28->19->32->4->36->2->31->29->12->0->8->6->10->1->35->9->23->22->3->26->25->16->5->21->15->11->20->37->33->30->18->24->17->34->27->14->38->7->13'
individuo_str2 = '22->20->25->38->4->19->34->17->16->30->35->14->10->11->33->23->39->24->0->31->6->21->15->7->13->28->12->1->9->5->3->8->26->29->36->18->32->2->27->37->22'
padre1 = list(map(int,individuo_str1.split("->")))
padre2 = list(map(int,individuo_str2.split("->")))


hijo1,hijo2 = cruce_ordenado_doble(padre1,padre2)
print("Padre 1:",padre1)
print("Padre 2:",padre2)
print()
print("Hijo 1:",hijo1)
print("Hijo 2:",hijo2)

print(evaluar_factibilidad('->'.join(map(str, hijo2))))


hijo1 =  padre1[1:corte1] + padre2[corte1:numeroNodos - 1] 
hijo2 =  padre2[1:corte1] + padre1[corte1:numeroNodos - 1]   

#insertamos primeros y ultimos nodos
hijo1.append(padre1[-1])
hijo2.append(padre2[-1])

hijo1.insert(0,padre1[0])
hijo2.insert(0,padre2[0])

print(padre1)
print(padre2)

print()

print(hijo1)
print(hijo2)
"""







