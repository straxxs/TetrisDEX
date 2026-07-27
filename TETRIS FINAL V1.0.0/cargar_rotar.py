from matriz import *
from tetris import *

def cargar_piezas():
    """
    Lee el archivo piezas.txt y devuelve todas las piezas con sus rotaciones.
    Cada pieza y rotación es una tupla de coordenadas (x, y) enteras.
    """
    piezas = []

    archivo=open("archivos_de_texto/piezas.txt", "r",)
    for linea in archivo:
        linea = linea.strip()
        # Quitar comentarios al final de la línea y separar rotaciones por espacios
        partes = linea.strip().split()
        partes.pop()
        partes.pop()
        rotaciones = []
        for rotacion in partes:
            bloques = []
            for bloque in rotacion.split(";"):
                x, y = bloque.split(",")
                bloques.append((int(x), int(y)))
            rotaciones.append(tuple(bloques))
        piezas.append(tuple(rotaciones))

    return tuple(piezas)


def rotar(pieza_en_juego, juego):
    """
    Gira la pieza actual según las rotaciones definidas en piezas.txt.
    Mantiene su posición actual y evita rotar si choca o se sale del tablero.
    """

    todas_las_piezas = cargar_piezas()

    # Tomar el primer bloque como referencia
    referencia_x = pieza_en_juego[0][0]
    referencia_y = pieza_en_juego[0][1]

    # Hacer una versión centrada de la pieza actual
    forma_actual = []
    for (x, y) in pieza_en_juego:
        forma_actual.append((x - referencia_x, y - referencia_y))

    # Buscar a qué tipo de pieza pertenece
    for rotaciones in todas_las_piezas:
        for i in range(len(rotaciones)):
            forma_guardada = []
            for (x, y) in rotaciones[i]:
                forma_guardada.append((x - rotaciones[i][0][0], y - rotaciones[i][0][1]))

            # Si coincide con la forma actual, buscar la siguiente rotación
            if forma_guardada == forma_actual:
                proxima = (i + 1) % len(rotaciones)
                nueva_forma = rotaciones[proxima]

                # Mover la nueva forma a la posición actual
                pieza_rotada = []
                for (x, y) in nueva_forma:
                    pieza_rotada.append((x + referencia_x, y + referencia_y))


                intento=0
                max_intentos=3
                cant_superf_validas=0
                
                                                        
                while not(intento>max_intentos):
                    
                    for (x, y) in pieza_rotada:
                        if not(hay_superficie(juego, x, y)):
                            cant_superf_validas+=1
                        else:
                            return pieza_en_juego
                    if cant_superf_validas!=4:    
                        es_none=trasladar_pieza(pieza_rotada,-intento,0)
                        if es_none==None:
                            intento+=1
                        else:
                            return trasladar_pieza(pieza_rotada,-intento,0)
                        cant_superf_validas=0
                        
                return pieza_actual
                

    # Si no se encontró una rotación, dejar la pieza igual
    return pieza_en_juego
