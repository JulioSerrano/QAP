import numpy
import random
import math
import matplotlib.pyplot as plt

# Funciones

# Función que lee los archivos de dsistancia y flujo
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

# Función que genera una solución alatoria
def solucionAleatoria(instalaciones):
    solucion = list(range(1, instalaciones + 1))
    random.shuffle(solucion)
    return solucion


# Función que evalúa la función objetivo
def funcionObjetivo(solucion, matriz_flujos, matriz_distancia):
    n = len(solucion)
    suma = 0
    for i in range(n):
        for j in range(n):
            suma = suma + matriz_flujos[i,j] * matriz_distancia[solucion[i] - 1,solucion[j] - 1]
    return suma


# Función que genera un vecino
def generarVecino(vecino):
    i = random.randint(2, len(vecino) - 1)
    j = random.randint(0, len(vecino) - i)
    vecino[j: (j + i)] = reversed(vecino[j: (j + i)])
    return(vecino)


# función que genera un vecino
def probablidadAceptacion(delta, temperatura_actual):
    probabilidad = math.e ** -(delta/temperatura_actual)
    return probabilidad


# Funcion que grafica los valores de la solución objetivo
def graficar(valores_objetivo, lista_mejors, lista_probabilidades, mejor_objetivo):
    plt.figure(1)
    plt.subplot(3, 1, 1)
    graficoMejores = plt.plot(lista_mejors)
    plt.setp(graficoMejores,"linestyle","none","marker","s","color","b","markersize","1")
    plt.title(u"Simulated annealing QAP") 
    plt.ylabel(u"Valor objetivo")
    plt.subplot(3, 1, 2)
    grafico = plt.plot(valores_objetivo)
    plt.setp(grafico,"linestyle","none","marker","s","color","r","markersize","1")
    plt.ylabel(u"Valor actual")
    plt.subplot(3, 1, 3)
    grafico = plt.plot(lista_probabilidades)
    plt.setp(grafico,"linestyle","none","marker","s","color","g","markersize","1")
    plt.ylabel(u"Probabilidad")
    plt.xlabel(u"Valor óptimo : " + str(mejor_objetivo))
    return True


#----------------- inicialización de variables --------------------------












# -------------- algoritmo SA ---------------------

def SimulatingAnniling(temperatura_actual, temperatura_minima, estado_equilibrio, enfriamiento, alpha, beta):
    distancias = "DChr12a"
    flujos = "FChr12a"
    # lectura archivo
    matriz_distancia = numpy.array(leeArchivo(distancias))
    matriz_flujos = numpy.array(leeArchivo(flujos))
    solucion_inicial = solucionAleatoria(len(matriz_distancia))
    solucion_actual = solucion_inicial.copy() 
    mejor_solucion = solucion_actual.copy()
    objetivo_actual = funcionObjetivo(mejor_solucion, matriz_flujos, matriz_distancia)
    mejor_objetivo = objetivo_actual
    lista_objetivos = [objetivo_actual]
    lista_mejores = [objetivo_actual]
    lista_probabilidades = []

    while temperatura_actual > temperatura_minima:
        i = 0
        while i < estado_equilibrio:
            solucion_candidato = generarVecino(solucion_actual)
            objetivo_candidata = funcionObjetivo(solucion_candidato, matriz_flujos, matriz_distancia)
            delta = objetivo_candidata - objetivo_actual
            if delta < 0:
                solucion_actual = solucion_candidato.copy()
                objetivo_actual = objetivo_candidata
                if objetivo_candidata < mejor_objetivo:
                    mejor_objetivo = objetivo_candidata
                    mejor_solucion = solucion_candidato.copy()
            else:
                probabilidad = probablidadAceptacion(delta, temperatura_actual)
                lista_probabilidades.append(probabilidad)
                if random.random() < probabilidad:
                    solucion_actual = solucion_candidato.copy()
                    objetivo_actual = objetivo_candidata
            lista_mejores.append(mejor_objetivo)
            lista_objetivos.append(objetivo_actual) 

            print(f"Temperatura: {temperatura_actual} - Objetivo:actual: {objetivo_actual} - Mejor objetivo: {mejor_objetivo}")
            i = i + 1
        if enfriamiento == "lineal":
            temperatura_actual = temperatura_actual - beta
        else:
            temperatura_actual = temperatura_actual * alpha 
    
    return mejor_objetivo


# # Gráficos
# graficar(lista_objetivos, lista_mejores, lista_probabilidades, mejor_objetivo)
# plt.show()



# ------------------ PRUEBAS -------------------

pruebas = {
    'temperatura_actual':[
        {
            'temperatura_actual': 1000000,
            'temperatura_minima': 0.001,
            'estado_equilibrio': 20,
            'enfriamiento': "geometrico",
            'alpha': 0.99,
            'beta': 0.99
        },
        {
            'temperatura_actual': 500000,
            'temperatura_minima': 0.001,
            'estado_equilibrio': 20,
            'enfriamiento': "geometrico",
            'alpha': 0.99,
            'beta': 0.99
        },
        {
            'temperatura_actual': 100000,
            'temperatura_minima': 0.001,
            'estado_equilibrio': 20,
            'enfriamiento': "geometrico",
            'alpha': 0.99,
            'beta': 0.99
        },
    ],
    'alpha':[
        {
            'temperatura_actual': 1000000,
            'temperatura_minima': 0.001,
            'estado_equilibrio': 20,
            'enfriamiento': "geometrico",
            'alpha': 0.99,
            'beta': 0.99
        },
        {
            'temperatura_actual': 1000000,
            'temperatura_minima': 0.001,
            'estado_equilibrio': 20,
            'enfriamiento': "geometrico",
            'alpha': 0.8,
            'beta': 0.99
        },
        {
            'temperatura_actual': 1000000,
            'temperatura_minima': 0.001,
            'estado_equilibrio': 20,
            'enfriamiento': "geometrico",
            'alpha': 0.7,
            'beta': 0.99
        },
    ],
}


def ejecutarPrueba(tipo):
    cantidad_pruebas = 30
    data = []
    labels = []
    for prueba in pruebas[tipo]:
        temperatura_actual = prueba['temperatura_actual']
        temperatura_minima = prueba['temperatura_minima']
        estado_equilibrio = prueba['estado_equilibrio']
        enfriamiento = prueba['enfriamiento']
        alpha = prueba['alpha']
        beta = prueba['beta']

        mejores_valores = []
        i = 0 
        while i < cantidad_pruebas:
            mejor_valor = SimulatingAnniling(temperatura_actual, temperatura_minima, estado_equilibrio, enfriamiento, alpha, beta)
            mejores_valores.append(mejor_valor)
            i += 1

        data.append(mejores_valores)
        labels.append(f"{tipo}: {prueba[tipo]}")

    plt.boxplot(data, labels=labels)
    plt.title(tipo)
    plt.ylabel('Función objetivo')
    plt.savefig(f'./resultados/SA/{tipo}.png')


ejecutarPrueba('temperatura_actual')
ejecutarPrueba('alpha')