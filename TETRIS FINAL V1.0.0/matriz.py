def crear_matriz(filas, columnas):
    """
    Recibe: la cantidad de filas y columnas de la matriz a crear.
    Proceso: Crea una matriz de dimensiones dadas por la cantidad de filas y columnas.
    Salida: Devuelve una estructura de matriz con las dimensiones recibidas.
    """
    matriz = []

    for i in range(filas):
        matriz.append([])
        for j in range(columnas):
            matriz[i].append(0)

    return matriz

def mostrar_matriz(matriz):
    """
    Recibe: una estructura de matriz.
    Proceso: Imprime cada fila de la matriz.
    Devuelve: None
    """

    for i in range(len(matriz)):
        print(matriz[i])

def insertar_valor_matriz(matriz: list, fila: int, columna: int, valor):
    """
    Recibe: una estructura matriz, el nro. de fila, el nro. de columna y el valor a ingresar a matriz.
    Proceso: inserta el valor dado en una posicion determinada.
    Devuelve: None 
    """

    matriz[fila][columna] = valor

def obtener_dimensiones(matriz):
    """
    Recibe: una matriz.
    Proceso: toma el largo y el ancho de las filas y columnas de la matriz recibida.
    Devuelve: una tupla (cantidad de filas, cantidad de columnas)
    """
    return len(matriz), len(matriz[0])

def sumar_matrices(matriz_1, matriz_2):
    """
    Recibe: dos estructuras de matrices.
    Proceso: Si las matrices poseen las mismas dimensiones, la funcion suma componente a componente los elementos de ambas.
    Devuelve: una nueva matriz resultante de la suma de componente a componente de las matrices recibidas. Caso contrario devuelve None.
    """

    if not(obtener_dimensiones(matriz_1) == obtener_dimensiones(matriz_2)):
        return None
    
    filas, columnas = obtener_dimensiones(matriz_1)
    matriz = crear_matriz(len(matriz_1), len(matriz_1[0]))

    for fila in range(filas):
        for columna in range(columnas):
            matriz[fila][columna] = matriz_1[fila][columna] + matriz_2[fila][columna]

    return matriz