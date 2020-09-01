import random
import numpy
import math
import matplotlib.pyplot as plt


# --------------- DEFINICION DE FUNCIONES  -----------------------


# Función que lee los archivos de distancia y flujo
def leeArchivo(nombre):
    nombre = "./archivos/" + nombre + ".txt"
    archivo = open(nombre, 'r')
    matriz = []
    fila = []
    for linea in archivo:
        fila = linea.split()
        lista_fila = []
        for elemento in fila:
            lista_fila.append(int(elemento))
        matriz.append(lista_fila)
    archivo.close()
    return matriz


# Funcion que genera una solucion aleatoria a partir de numero de instalaciones
def solucionAleatoria(instalaciones):
    solucion = list(range(1, instalaciones + 1))
    random.shuffle(solucion)
    return solucion

# Funcion que obtiene la poblacion inicial


# Función que genera una población inicial segun la cantidad de individuos
def poblacionInicial(individuos, instalaciones):
    i = 0
    poblacion = []
    for i in range(individuos):
        individuo = solucionAleatoria(instalaciones)
        while individuo in poblacion:
          individuo = solucionAleatoria(instalaciones)
        poblacion.append(individuo)
    return poblacion


# Función que obtiene el valor de una solucion
def funcionObjetivo(solucion, matriz_distancia, matriz_flujo):
    n = len(solucion)
    suma = 0
    for i in range(n):
        for j in range(n):
            suma = suma + matriz_flujo[i, j] * \
                matriz_distancia[solucion[i] - 1, solucion[j] - 1]
    return suma


# Funcion que evalua la cada uno de los individuos en la funcion objetivo
def evaluarPoblacion(poblacion, matriz_flujos, matriz_distancia):
    valores_poblacion = []
    for i in poblacion:
        valor = funcionObjetivo(i, matriz_flujos, matriz_distancia)
        valores_poblacion.append(valor)

    return valores_poblacion


# Fución que obtiene el mejor individuo evaluando las funciones objetivos de la poblacion
def mejorIndividuo(individuos,  matriz_flujos, matriz_distancia):
    valores_poblacion = evaluarPoblacion(individuos, matriz_flujos, matriz_distancia)
    indice_mejor_valor = valores_poblacion.index(min(valores_poblacion))

    return individuos[indice_mejor_valor]


# Seleccion de individuos creado torneos y eligiendo el mejor para generar una nueva población
def seleccionTorneo(individuos, tamano_torneo, cantidad_torneos, matriz_flujos, matriz_distancia):
    nueva_poblacion = []
    i = 0
    while i < cantidad_torneos:
        torneo = []
        j = 0
        while j < tamano_torneo:
            indice = random.randint(0, (len(individuos) - 1))
            torneo.append(individuos[indice])
            j = j + 1

        mejor_individuo = mejorIndividuo(torneo, matriz_flujos, matriz_distancia)
        nueva_poblacion.append(mejor_individuo)
        i = i + 1
    
    return nueva_poblacion


# Funcion que genera un hijo a partir de dos padres a través aplicando one order crosover
# def combinacionPadres(primer_padre, segundo_padre, primer_indice, segundo_indice):
#     hijo = [0] * len(primer_padre)
#     for i in range(primer_indice, segundo_indice + 1):
#         hijo[i] = primer_padre[i]

#     j = 0
#     for i in range(0, len(primer_padre)):
#         if j > len(primer_padre)-1:
#             break
#         if j == primer_indice:
#             j = segundo_indice + 1

#         if hijo[j] == 0 and segundo_padre[i] not in hijo:
#             hijo[j] = segundo_padre[i]
#             j = j + 1

#     return hijo

def combinacionPadres(primer_padre, segundo_padre, primer_indice, segundo_indice):
    hijo = [0] * len(primer_padre)
        
    #Child1
    herencia = primer_padre[primer_indice:segundo_indice]
    hijo[primer_indice:segundo_indice] = herencia
    
    parent2_values = []
    i = 0
    for i in range(len(segundo_padre)):
        if segundo_padre[i] not in herencia:
            parent2_values.append(segundo_padre[i])
    
    k = 0
    for i in range(len(hijo)):
        if hijo[i] == 0:
            hijo[i] = parent2_values[k]
            k += 1
    return hijo


# Funcion que intercambia dos valores aleatorios


def swap(solucion):
    i = random.randint(2, len(solucion) - 1)
    j = random.randint(0, len(solucion) - i)
    solucion[j: (j + i)] = reversed(solucion[j: (j + i)])
    return(solucion)

# Funcion que muta la solucion ingresada segun una probabilidad dada


def mutarHijo(hijo, chance_mutacion):
    chance = random.uniform(0, 1)
    # chance de mutacion
    if chance <= chance_mutacion:
        # Swap mutation
        hijo = swap(hijo)
    return hijo


# Se crean el numero de hijos indicado usando one order crosover y mutacion
def reproducirPoblacion(poblacion, numero_hijos, chance_mutacion):
    numero_individuos = len(poblacion)
    # Intercambio 1 order crossover entre el primer tercio de la lista y el ultimo tercio
    primer_indice = math.floor(len(poblacion[0]) * random.uniform(0.1, 0.4))
    segundo_indice = math.floor(len(poblacion[0]) * random.uniform(0.6, 0.8))

    hijos = []
    i = 0
    while i < math.floor(numero_hijos / 2):
        # indice para elegir a un padre aleatorio
        indice_primer_padre = random.randint(0, (numero_individuos - 1))
        indice_segundo_padre = random.randint(0, (numero_individuos - 1))

        primer_padre = poblacion[indice_primer_padre]
        segundo_padre = poblacion[indice_segundo_padre]

        # combinacion one order y mutacion de hijo
        primer_hijo = combinacionPadres(
            primer_padre, segundo_padre, primer_indice, segundo_indice)
        primer_hijo = mutarHijo(primer_hijo, chance_mutacion)
        segundo_hijo = combinacionPadres(
            segundo_padre, primer_padre, primer_indice, segundo_indice)
        segundo_hijo = mutarHijo(segundo_hijo, chance_mutacion)

        # agregar hijos a la lista
        hijos.append(primer_hijo)
        hijos.append(segundo_hijo)

        i = i + 1

    return hijos


# TODO arreglar
# Funcion que mezcla las soluciones padres con los hijos eligiendo los mejores de cada conjunto
def reemplazo(padres, hijos, matriz_flujos, matriz_distancia):
    valores_padres = evaluarPoblacion(padres, matriz_flujos, matriz_distancia)
    valores_hijos = evaluarPoblacion(hijos, matriz_flujos, matriz_distancia)

    zipped_lists = zip(valores_padres, padres)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    valores_padres, padres = [list(tuple) for tuple in tuples]

    zipped_lists = zip(valores_hijos, hijos)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    valores_hijos, hijos = [list(tuple) for tuple in tuples]

    indice_padres = math.floor(len(padres) * 0.4)
    indice_hijos = math.floor(len(padres) * 0.6)

    return padres[0: indice_padres] + hijos[0:indice_hijos]


# Funcion que grafica los valores de la solución objetivo
def graficar(lista_mejores):
    plt.figure(1)
    plt.subplot(3, 1, 1)
    grafico_mejores = plt.plot(lista_mejores)
    plt.setp(grafico_mejores, "linestyle", "none",
             "marker", "s", "color", "b", "markersize", "1")
    plt.title(u"Simulated annealing QAP")
    plt.ylabel(u"Valor objetivo")
    return True




def algoritmoGenetico(generaciones_totales, cantidad_torneos, chance_mutacion, cantidad_hijos, tamano_torneo, individuos):
    archivo_distancia = "DChr12a"
    archivo_flujos = "FChr12a"
    matriz_distancia = numpy.array(leeArchivo(archivo_distancia))
    matriz_flujos = numpy.array(leeArchivo(archivo_flujos))
    poblacion_inicial = poblacionInicial(individuos, len(matriz_distancia))
    poblacion = poblacion_inicial.copy()
    lista_mejores = []
    
    
    generacion = 0
    while generacion < generaciones_totales:
        print(f"\n\n---- Generación: {generacion} --")
        
        # ---- Seleccion de padres ----
        poblacion_torneo = seleccionTorneo(poblacion, tamano_torneo, cantidad_torneos, matriz_flujos, matriz_distancia)

        # ---- Reproducción ----
        hijos = reproducirPoblacion(poblacion_torneo, cantidad_hijos, chance_mutacion)

        # ---- Reemplazo --------
        poblacion_reemplazo = reemplazo(poblacion_torneo, hijos, matriz_flujos, matriz_distancia)

        print("----MEJOR INDIVIDUO ----")
        mejor_individuo = mejorIndividuo(poblacion_reemplazo, matriz_flujos, matriz_distancia)
        print(mejor_individuo)

        print("---- Mejor valorrr -----")
        mejor_valor = funcionObjetivo(mejor_individuo, matriz_flujos, matriz_distancia)
        print(mejor_valor)  
        lista_mejores.append(mejor_valor)
        poblacion = poblacion_reemplazo.copy()
        generacion += 1

    return mejor_valor

#--------------- PRUEBAS ----------------

def ejecutarPrueba(tipo):
    cantidad_pruebas = 30
    data = []
    labels = []
    for prueba in pruebas[tipo]:
        generaciones_totales = prueba['generaciones_totales']
        cantidad_torneos = prueba['cantidad_torneos']
        chance_mutacion = prueba['chance_mutacion']
        cantidad_hijos = prueba['cantidad_hijos']
        tamano_torneo = prueba['tamano_torneo']
        individuos = prueba['individuos']

        mejores_valores = []
        i = 0 
        while i < cantidad_pruebas:
            mejor_valor = algoritmoGenetico(generaciones_totales, cantidad_torneos, chance_mutacion, cantidad_hijos, tamano_torneo, individuos)
            mejores_valores.append(mejor_valor)
            i += 1

        data.append(mejores_valores)
        labels.append(f"{tipo}: {prueba[tipo]}")

    plt.boxplot(data, labels=labels)
    plt.title(tipo)
    plt.ylabel('Función objetivo')
    plt.savefig(f'./resultados/GA/{tipo}.png')


pruebas = {
    'individuos':[
        {
            'generaciones_totales': 1,
            'cantidad_torneos': 100,
            'chance_mutacion': 0.1,
            'cantidad_hijos': 50,
            'tamano_torneo': 20,
            'individuos': 400
        },
        {
            'generaciones_totales': 1,
            'cantidad_torneos': 100,
            'chance_mutacion': 0.1,
            'cantidad_hijos': 50,
            'tamano_torneo': 20,
            'individuos': 200
        },
        {
            'generaciones_totales': 1,
            'cantidad_torneos': 100,
            'chance_mutacion': 0.1,
            'cantidad_hijos': 50,
            'tamano_torneo': 20,
            'individuos': 100
        },
    ],
    'chance_mutacion':[
        {
            'generaciones_totales': 1,
            'cantidad_torneos': 100,
            'chance_mutacion': 0.5,
            'cantidad_hijos': 50,
            'tamano_torneo': 20,
            'individuos': 200
        },
        {
            'generaciones_totales': 1,
            'cantidad_torneos': 100,
            'chance_mutacion': 0.3,
            'cantidad_hijos': 50,
            'tamano_torneo': 20,
            'individuos': 200
        },
        {
            'generaciones_totales': 1,
            'cantidad_torneos': 100,
            'chance_mutacion': 0.1,
            'cantidad_hijos': 50,
            'tamano_torneo': 20,
            'individuos': 200
        },
    ],
}



ejecutarPrueba('individuos')
ejecutarPrueba('chance_mutacion')
