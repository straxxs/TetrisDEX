from matriz import *
import random
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo  0
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag) 1
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z) 2
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea) 3
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L 4
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L 5
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T 6
)


def generar_pieza(pieza=None):
    """ Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc."""
    if pieza==None:
        return PIEZAS[random.randint(0, len(PIEZAS)-1)]
    else:
        return PIEZAS[pieza]

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_aux=[]
    for coordenada in range(0,len(pieza),1):
        if pieza[coordenada][0]+dx>=ANCHO_JUEGO or pieza[coordenada][0]+dx<0 or pieza[coordenada][1]+dy>=ALTO_JUEGO:
            return None
        pieza_aux.append((pieza[coordenada][0]+dx,pieza[coordenada][1]+dy))
    return tuple(pieza_aux)


def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    generar_pieza(). Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    pieza_inicial=trasladar_pieza(pieza_inicial,ANCHO_JUEGO//2,0)
    return ([[0 for i in range(ANCHO_JUEGO)] for i in range(ALTO_JUEGO)],pieza_inicial)


def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    
    return len(juego[0][0]),len(juego[0])


def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """ 
    
    return juego[1]

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    if y>17 or x<0 or x>8:
        return True
    if juego[0][y][x]==2:
        return True
    return False 
        

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    for x,y in juego[1]:
        if hay_superficie(juego,x+direccion,y):
            return juego
    nueva_pieza=trasladar_pieza(pieza_actual(juego),direccion,0)
    if nueva_pieza==None:
        return juego
    return juego[0],nueva_pieza




def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    grilla,pieza_actual=juego
    if terminado(juego):
        return juego, False, 0
    
    
    cambiar_pieza=False
    for coordenada in range(len(pieza_actual)):
        if(hay_superficie(juego, pieza_actual[coordenada][0],pieza_actual[coordenada][1]+1)):
            cambiar_pieza=True
    if not(cambiar_pieza):
        return (grilla,trasladar_pieza(pieza_actual,0,1)),cambiar_pieza, 0
    else:
        grilla=consolidar_pieza(pieza_actual, grilla)
        pieza_actual=cambiar_pieza_actual(siguiente_pieza)
        grilla, cant_filas=eliminar_filas(grilla)
        
    juego=list(juego)        
    juego=grilla,pieza_actual
    juego=tuple(juego)
    return juego, cambiar_pieza,cant_filas

def eliminar_filas(grilla):
    """
    Elimina una fila completa y agrega una nueva fila vacía en la parte superior de la grilla 
    y devuelve la grilla actualizada.
    """
    filas_a_eliminar=0
    for i in range(ALTO_JUEGO):    
        for direccion_y in range(ALTO_JUEGO):
            cont=0
            hay_que_eliminar=False
            for direccion_x in range(ANCHO_JUEGO):
                if grilla[direccion_y][direccion_x]==2:
                    cont+=1
            if cont==ANCHO_JUEGO:
                hay_que_eliminar=True
                filas_a_eliminar+=1
                break
        
        if hay_que_eliminar:    
            grilla.pop(direccion_y)
            fila_nueva=[0 for i in range(ANCHO_JUEGO)]
            grilla.insert(0,(fila_nueva))
            
    return grilla, filas_a_eliminar


def cambiar_pieza_actual(siguiente_pieza):
    """
    Cambia la pieza actual por la siguiente pieza y la posiciona en el centro arriba de todo y la devuelve.
    """
    pieza_actual=trasladar_pieza(siguiente_pieza,ANCHO_JUEGO//2,0)
    return pieza_actual

def consolidar_pieza(pieza_actual, grilla):
    """
    Consolida la pieza actual con la superficie del juego y devuelve la grilla actualizada.
    """
    for coordenada in range(len(pieza_actual)):
            y_pieza,x_pieza=pieza_actual[coordenada][1],pieza_actual[coordenada][0]
            grilla[y_pieza][x_pieza]=2
    return grilla
    

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    pieza=pieza_actual(juego)
    for i in range(len(pieza)):
        if(hay_superficie(juego, pieza[i][0],pieza[i][1])) and pieza[0][1]==0:
            return True
    return False