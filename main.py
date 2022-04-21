import sys
import matplotlib.pyplot as plt
from random import sample, choice, shuffle


def tableGenerator(number_reserves):
    wing_types = map(lambda x: x + '-Reserva', ['JUAN', 'PEPE', 'MARIA', 'LAIA', 'MONTSE', 'PAULA'])
    L = list(wing_types)
    free_pos = sample(range(number_reserves), number_reserves >> 1)
    position = 0

    global solution
    solution = min(free_pos)

    while position <= number_reserves:
        if position not in free_pos:
            yield choice(L), str(position)
        position += 1


def reserveList(number_reserves):
    reserve_list = [i for i in tableGenerator(number_reserves * 2)]

    reserve_list = reserve_list[:number_reserves]

    shuffle(reserve_list)

    return reserve_list, solution


def bookerineManagement_iterativo(reserves):
    array = []
    idTable = -1
    array = (createGoodArray(reserves))
    array.sort()
    # print("ite", array)
    for i in range(0, len(array)):
        idTable = i
        if idTable != array[i]:
            return idTable

    return idTable + 1  # SOLO SE LLEGA CUANDO NO HAY MÁS ESPACIO, TODAS LAS MESAS  ESTAN RESERVADAS


def createGoodArray(array):
    newArray = []

    for i in range(0, len(array)):
        newArray.append(int(array[i][1]))
        i += 1

    return newArray


def bookerineManagement_recursivo(reserves):
    array = (createGoodArray(reserves))
    array.sort()
    return recursivoNoFinal(array, 0)  # Inicializar con el número de mesa más cercano a la cocina


def recursivoNoFinal(array, idTable):
    if not array:
        return idTable
    if idTable != array[0]:
        return idTable
    else:
        return recursivoNoFinal(array[1:], idTable + 1)


def calcular_temps_iterativo():
    import timeit
    temps = []
    for x in range(1, 200, 10):
        out_reserves = reserveList(x)
        reserves = out_reserves[0]
        temps.append((x, timeit.timeit("bookerineManagement_iterativo(" + str(reserves) + ")",
                                       setup="from __main__ import bookerineManagement_iterativo")))
    return temps


def calcular_temps_recursivo():
    import timeit
    temps = []
    for x in range(1, 200, 10):
        out_reserves = reserveList(x)
        reserves = out_reserves[0]
        temps.append((x, timeit.timeit("bookerineManagement_recursivo(" + str(reserves) + ")",
                                       setup="from __main__ import bookerineManagement_recursivo")))
    return temps


def crear_grafica(x_list, y_list):
    plt.scatter(x_list, y_list)
    plt.show()


def costEmpiricalComputation():
    temps_iterativo = calcular_temps_iterativo()
    crear_grafica(*map(list, zip(*temps_iterativo)))

    temps_recursivo = calcular_temps_recursivo()
    crear_grafica(*map(list, zip(*temps_recursivo)))

    return 0


# Programa Principal para la generación de mesas y reservas dentro de un restaurante. Para ello, al programa deberemos
# de pasarle como argumentos el tamaño del restaurante en número de mesas.
if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit('Usage: ' + sys.argv[0] + ' <list_size>')

    out_reserves = reserveList(int(sys.argv[1]))
    reserves = out_reserves[0]
    idTable = bookerineManagement_iterativo(reserves)

    costEmpiricalComputation()

    if idTable == solution:
        print('Solucion Correcta')
    else:
        print('Solucion Incorrecta')
