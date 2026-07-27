from idiomas import cargar_idioma
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import gamelib
from tetris import *
import time
from matriz import *
import ast
from cargar_rotar import *
import platform
import pygame
import random
import tkinter as tk
import tkinter
import ctypes
import os 
from tkinter import filedialog, colorchooser

COLORES = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(50)]

def jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total):
    """Función principal que ejecuta el juego"""
    puntaje = 0
    if modo == 1 or modo == 4 or modo == 5 or modo == 6 or modo == 7 or modo == 8 or modo == 11 or modo == 12: 
        intervalo = 0.85
    elif modo == 2:  
        intervalo = 0.45
    elif modo == 3: 
        intervalo = 1.3
    
    gamelib.draw_begin()
    crear_ventana(sonido, on, vol)
    dibujar_grilla_y_controles(puntaje,intervalo, modo, imagen, color, color_es, idioma, color_guia)
    gamelib.draw_end()
    juego=crear_juego(generar_pieza())
    pieza=pieza_actual(juego)
    siguiente_pieza=generar_pieza() 
    pieza_futura = generar_pieza()  
    pieza_futura2 = generar_pieza()
    
    ultimo_avance = time.time()
    tiempo_desde_inicio=time.time()
    pausa=False
    a=0
    contador=0
    while gamelib.loop():
        gamelib.draw_begin()
        #Dibuja la grilla, piezas consolidadas, la siguiente pieza y la pieza fantasma
        dibujar_grilla_y_controles(puntaje,intervalo, modo,imagen,color, color_es, idioma, color_guia)
        
        #Inicializa la variable cambiar_pieza como falsa
        cambiar_pieza=False

        #Avanza el estado de juego cada cierto tiempo determinado por la variable intervalo
        ahora=time.time()

        if not pausa:
            pygame.mixer.music.unpause()
            if ahora-ultimo_avance >= intervalo:
               ultimo_avance=ahora
               juego, cambiar_pieza, puntaje,intervalo=avanzar_estado_juego(juego,siguiente_pieza,puntaje,intervalo)

            #Cada cierto tiempo va redciendo el intervalo de tiempo al 95% para acelerar el juego gradualmente
            if modo == 1 or modo == 4 or modo == 5 or modo == 6 or modo == 7 or modo == 11:
              if time.time() - tiempo_desde_inicio >= 30:
                 intervalo*=0.9
                 tiempo_desde_inicio=time.time()
            if modo == 2:   
              if time.time() - tiempo_desde_inicio >= 20:
                 intervalo*=0.45
                 tiempo_desde_inicio=time.time()  
            if modo == 3:
              if time.time() - tiempo_desde_inicio >= 45:
                 intervalo*=0.9
                 tiempo_desde_inicio=time.time()   
            if modo == 8 or modo == 12:
                tiempo_restante = tiempo_total - int(time.time() - tiempo_desde_inicio)
                gamelib.draw_text(f"Tiempo: {tiempo_restante}s", ANCHO//1.3, ALTO // 38.7, fill=color_guia, size=int(ALTO * 0.02567))
       
        if modo == 1 or modo == 2 or modo == 3 or modo == 5 or modo == 6 or modo == 7 or modo == 8 or modo == 11 or modo == 12:
         for event in gamelib.get_events():
            if event.type == gamelib.EventType.KeyPress:
                if not pausa and not(terminado(juego)):

                        #Si se apreta la tecla "s" o "Down" se avanza el estado de juego
                        if event.key == "Down" or event.key == "s":
                            juego, cambiar_pieza, puntaje,intervalo=avanzar_estado_juego(juego,siguiente_pieza, puntaje,intervalo)
                            ultimo_avance=time.time()

                        if event.key == "c":
                            gamelib.draw_rectangle(0, 0, ANCHO, ALTO, fill='gray20', outline='', width=0)
                            gamelib.draw_text(traducciones["cargar"], ANCHO//2, ALTO//2, anchor="center", fill="white", size=40)
                            time.sleep(1)
                            juego=list(juego)
                            juego,intervalo,puntaje=cargar_juego(modo)

                        if event.key == "g":
                            gamelib.draw_rectangle(0, 0, ANCHO, ALTO, fill='gray20', outline='', width=0)
                            gamelib.draw_text(traducciones["guardar"], ANCHO//2, ALTO//2, anchor="center", fill="white", size=40)
                            time.sleep(1)
                            guardar_juego(juego, intervalo, puntaje, modo)

                        #Si se apreta la tecla espacio la pieza avanza todas las posiciones de "y" que puede y se consolida
                        if event.key == "space":
                            while not(cambiar_pieza):
                                juego, cambiar_pieza, puntaje,intervalo=avanzar_estado_juego(juego,siguiente_pieza, puntaje,intervalo)

                        #Si se apreta la tecla "s" o "Left" la pieza se mueve a la izquierda
                        if event.key == "Left" or event.key == "a":
                            juego=mover(juego,IZQUIERDA)

                        
                        #Si se apreta la tecla "d" o "Right" la pieza se mueve a la derecha
                        if event.key == "Right" or event.key == "d":
                            juego=mover(juego,DERECHA)

                        if event.key == "Up" or event.key == "w":
                            juego=list(juego)
                            juego[1]=rotar(juego[1], juego)
                            juego=tuple(juego)
                            
                            
                if event.key == "p":
                    pausa = not pausa
                #Al apretar la tecla "n" se ejecuta la funcion jugar() inicializando un nuevo juego
                if event.key == "n":
                    jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total) 
                    return
                #Si se apretap la tecla Escape se sale del programa
                if event.key == "Escape":
                    pygame.mixer.music.stop()
                    gamelib.draw_rectangle(0, 0, ANCHO, ALTO, fill='gray20', outline='', width=0)
                    gamelib.draw_text(traducciones["salir"], ANCHO//2, ALTO//2, anchor="center", fill="white", size=40)
                    time.sleep(0.8)
                    if b == 0:
                        pygame.mixer.music.load("sonido/Angry_bird.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(-1)
                        return
                    else:
                        if on == 1 and b == 1:
                            pygame.mixer.music.load("sonido/inicio.mp3")
                            pygame.mixer.music.set_volume(1)
                            pygame.mixer.music.play(-1)
                            return
                        if on == 0:
                            pygame.mixer.music.stop()
                            return

        if modo == 4:
         for event in gamelib.get_events():
            if event.type == gamelib.EventType.KeyPress:
                if not pausa and not(terminado(juego)):

                        #Si se apreta la tecla "s" o "Down" se avanza el estado de juego
                        if event.key == "Down" or event.key == "s":
                            juego=list(juego)
                            juego[1]=rotar(juego[1], juego)
                            juego=tuple(juego)  
                           

                        if event.key == "c":
                            gamelib.draw_rectangle(0, 0, ANCHO, ALTO, fill='gray20', outline='', width=0)
                            gamelib.draw_text(traducciones["cargar"], ANCHO//2, ALTO//2, anchor="center", fill="white", size=40)
                            time.sleep(1)
                            juego=list(juego)
                            juego,intervalo,puntaje=cargar_juego(modo)

                        if event.key == "g":
                            gamelib.draw_rectangle(0, 0, ANCHO, ALTO, fill='gray20', outline='', width=0)
                            gamelib.draw_text(traducciones["guardar"], ANCHO//2, ALTO//2, anchor="center", fill="white", size=40)
                            time.sleep(1)
                            guardar_juego(juego, intervalo, puntaje, modo)

                        #Si se apreta la tecla espacio la pieza avanza todas las posiciones de "y" que puede y se consolida
                        if event.key == "space":
                            juego, cambiar_pieza, puntaje,intervalo=avanzar_estado_juego(juego,siguiente_pieza, puntaje,intervalo)
                            ultimo_avance=time.time()

                        #Si se apreta la tecla "s" o "Left" la pieza se mueve a la izquierda
                        if event.key == "Left" or event.key == "a":
                            juego=mover(juego,DERECHA)

                        #Si se apreta la tecla "d" o "Right" la pieza se mueve a la derecha
                        if event.key == "Right" or event.key == "d":
                            juego=mover(juego,IZQUIERDA)

                        if event.key == "p":
                            pausa = not pausa

                        if event.key == "Up" or event.key == "w":
                            while not(cambiar_pieza):
                                juego, cambiar_pieza, puntaje,intervalo=avanzar_estado_juego(juego,siguiente_pieza, puntaje,intervalo)

                if event.key == "Escape":
                    pygame.mixer.music.stop()
                    gamelib.draw_rectangle(0, 0, ANCHO, ALTO, fill='gray20', outline='', width=0)
                    gamelib.draw_text(traducciones["salir"], ANCHO//2, ALTO//2, anchor="center", fill="white", size=40)
                    time.sleep(0.8)
                    if b == 0:
                        pygame.mixer.music.load("sonido/Angry_bird.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(-1)
                        return
                    else:
                        if on == 1 and b == 1:
                            pygame.mixer.music.load("sonido/inicio.mp3")
                            pygame.mixer.music.set_volume(1)
                            pygame.mixer.music.play(-1)
                            return
                        if on == 0:
                            pygame.mixer.music.stop()
                            return
                #Si se apretap la tecla Escape se sale del programa
                if event.key == "n":
                    jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total) 
                    return
                    

        #Dibuja un nuevo estado de juego
        siguiente_pieza, pieza_futura, pieza_futura2=dibujar_nuevo_estado_juego(juego, cambiar_pieza, siguiente_pieza, pieza_fantasma, color_pieza, color_pieza_consolidada, color_pieza_siguiente, modo, pieza_futura, pieza_futura2)
        if pausa:# Dibujar una capa semitransparente (gris oscuro translúcido)
            pygame.mixer.music.pause()
            gamelib.draw_rectangle(0, 0, ANCHO, ALTO, fill='gray20', outline='', width=0)
            gamelib.draw_text(traducciones["pausa"], ANCHO//2, ALTO//2, anchor="center", fill="white", size=40)
            gamelib.draw_text(traducciones["continuar"], ANCHO//2, ALTO//1.8, anchor="center", fill="white", size=20)
        #Si el juego se termino cierra el programa
        if modo == 11:
            if terminado(juego):
                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                return
        if modo != 12 or modo!=8:
            if terminado(juego):
                pantalla_perdiste(puntaje, idioma, modo)
                if on == 1 and contador==0 and b == 1:
                    contador+=1
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sonido/mix_perdiste.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play()
                
                if b == 0 and contador == 0:
                    contador+=1
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sonido/Mama soy un angry bird saturado.mp3")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play()

                elif on==0:
                    pygame.mixer.music.stop()
                ordenar_ranking(modo)
                if a==0:
                    if event.key == "l":
                        nombre=gamelib.input("Ingrese su nombre:")
                        ranking(puntaje, nombre, modo)
                        a+=1 
        if modo == 8:
            if terminado(juego) or tiempo_restante <= 0:
                    pantalla_perdiste(puntaje, idioma, modo)
                    if on == 1 and contador==0 and b == 1:
                        contador+=1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("sonido/mix_perdiste.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play()
                    
                    if b == 0 and contador == 0:
                        contador+=1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("sonido/Mama soy un angry bird saturado.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play()

                    elif on==0:
                        pygame.mixer.music.stop()
                    ordenar_ranking(modo)
                    if a==0:
                        if event.key == "l":
                            nombre=gamelib.input("Ingrese su nombre:")
                            ranking(puntaje, nombre, modo)
                            a+=1 

        if modo == 12:
            if terminado(juego) or tiempo_restante <= 0:
                    pantalla_perdiste(puntaje, idioma, modo)
                    if on == 1 and contador==0 and b == 1:
                        contador+=1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("sonido/mix_perdiste.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play()
                    
                    if b == 0 and contador == 0:
                        contador+=1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("sonido/Mama soy un angry bird saturado.mp3")
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play()

                    elif on==0:
                        pygame.mixer.music.stop()

        gamelib.draw_end()
        
def ranking(puntaje, nombre, modo):
    """Guarda el puntaje de los modos en distintos archivos de textos para que no se mezclen """
    if modo == 1:
        rank = "archivos_de_texto/ranking_modo_normal.txt"
    if modo == 2:
        rank =  "archivos_de_texto/ranking_modo_rapido.txt"
    if modo == 3:
        rank = "archivos_de_texto/ranking_modo_lento.txt"
    if modo == 4: 
        rank = "archivos_de_texto/ranking_modo_invertido.txt"
    if modo == 5:
        rank = "archivos_de_texto/ranking_modo_rainbow.txt"
    if modo == 6:
        rank = "archivos_de_texto/ranking_modo_sin_pieza_actual.txt"
    if modo == 7:
        rank = "archivos_de_texto/ranking_modo_sin_pieza_consolidada.txt"
    if modo == 8:
        rank = "archivos_de_texto/ranking_modo_contrarreloj.txt"


    archivo=open(rank, mode="a")
    archivo.write(str(puntaje)+";"+str(nombre)+"\n")
    archivo.close()
    

def ordenar_ranking(modo):
    """ordena de mayor a menor los archivos de texto con su nombre y puntaje segun el modo"""
    lista_a_ordenar=[]
    punt_nom=[]
    if modo == 1:
        ord_rank = "archivos_de_texto/ranking_modo_normal.txt"
    if modo == 2:
        ord_rank =  "archivos_de_texto/ranking_modo_rapido.txt"
    if modo == 3:
        ord_rank = "archivos_de_texto/ranking_modo_lento.txt"
    if modo == 4: 
        ord_rank = "archivos_de_texto/ranking_modo_invertido.txt"
    if modo == 5:
        ord_rank = "archivos_de_texto/ranking_modo_rainbow.txt"
    if modo == 6:
        ord_rank = "archivos_de_texto/ranking_modo_sin_pieza_actual.txt"
    if modo == 7:
        ord_rank = "archivos_de_texto/ranking_modo_sin_pieza_consolidada.txt"
    if modo == 8:
        ord_rank = "archivos_de_texto/ranking_modo_contrarreloj.txt"
    
    archivo=open(ord_rank, mode="r")
    for linea in archivo:
        linea=linea.strip()
        punt_nom=linea.split(";")
        lista_a_ordenar.append((int(punt_nom[0]),punt_nom[1]))
        lista_a_ordenar.sort(reverse=True)
    
    for i in range(5):
        gamelib.draw_text("RANKING",ANCHO//2,60, font="italic",bold=True, size=40)
        gamelib.draw_text(f"{i+1}. {lista_a_ordenar[i][1]} = {lista_a_ordenar[i][0]}", ANCHO//2,100+30*i, size=15, anchor="center")
    archivo.close()
    
def guardar_juego(juego,intervalo, puntaje, modo ):
    
    if modo == 1:
        guardar = "archivos_de_texto/juego_guardado_normal.txt"
    if modo == 2:
        guardar = "archivos_de_texto/juego_guardado_rapido.txt"
    if modo == 3:
        guardar = "archivos_de_texto/juego_guardado_lento.txt"
    if modo == 4:
        guardar = "archivos_de_texto/juego_guardado_invertido.txt"
    if modo == 5:
        guardar = "archivos_de_texto/juego_guardado_rainbow.txt"
    if modo == 6:
        guardar = "archivos_de_texto/juego_guardado_sin_pieza_actual.txt"
    if modo == 7:
        guardar = "archivos_de_texto/juego_guardado_sin_pieza_consolidada.txt"
    if modo == 8:
        guardar = "archivos_de_texto/juego_guardado_contrarreloj.txt"

    archivo=open(guardar, mode="w")
    archivo.write(str(juego[0])+"\n")
    archivo.write(str(juego[1])+"\n")
    archivo.write(str(intervalo)+"\n")
    archivo.write(str(puntaje))
    archivo.close()


def cargar_juego(modo):
    if modo == 1:
        cargar = "archivos_de_texto/juego_guardado_normal.txt"
    if modo == 2:
        cargar = "archivos_de_texto/juego_guardado_rapido.txt"
    if modo == 3:
        cargar = "archivos_de_texto/juego_guardado_lento.txt"
    if modo == 4:
        cargar = "archivos_de_texto/juego_guardado_invertido.txt"
    if modo == 5:
        cargar = "archivos_de_texto/juego_guardado_no_look.txt"
    if modo == 6:
        cargar = "archivos_de_texto/juego_guardado_sin_pieza_actual.txt"
    if modo == 7:
        cargar = "archivos_de_texto/juego_guardado_sin_pieza_consolidada.txt"
    if modo == 8:
        cargar = "archivos_de_texto/juego_guardado_contrarreloj.txt"    
    
    archivo=open(cargar, mode="r")
    grilla_str=archivo.readline()
    pieza_str=archivo.readline()
    intervalo_str=archivo.readline()
    puntaje_str=archivo.readline()

    grilla_lista = ast.literal_eval(grilla_str)
    pieza = ast.literal_eval(pieza_str)
    grilla = list(list(fila) for fila in grilla_lista)
    intervalo = float(intervalo_str)
    puntaje = int(puntaje_str)
    return (grilla,pieza),intervalo, puntaje
    
# ---------------------------------------------------------------
# FUNCIONES DE DIBUJO 
# ---------------------------------------------------------------

def dibujar_pieza_fantasma(juego, modo):
    """Genera la pieza fantasma para saber donde va a caer la pieza actual"""

    #Inicializa los valores de desplazamiento, puede_bajar y guarda la pieza actual en pieza
    desplazamiento_abajo=0
    puede_bajar=True
    pieza=pieza_actual(juego)

    #Mientras la pieza pueda bajar se revisa abajo de la misma para ver si hay superficie
    while puede_bajar:
        for x,y in pieza:
            if hay_superficie(juego,x,y+desplazamiento_abajo+1):

                #Como sí la hay se guarda False en puede_bajar y se rompe el ciclo
                puede_bajar=False
                break

        #Como no la hay se suma 1 a desplazamiento
        desplazamiento_abajo+=1
    
    #Dibuja la pieza fantasma
    for x,y in pieza:
        x1=x
        y1=y+desplazamiento_abajo-1
        gamelib.draw_rectangle(base_x + x1 * 31 + x1,
                               base_y + y1 * 31 + y1,
                               base_x + (x1 + 1) * 31 + x1,
                               base_y + (y1 + 1) *31 + y1, 
                               fill="#a9d9e7", outline="white", width=1.5)
        if modo == 5:
            gamelib.draw_rectangle(base_x + x1 * 31 + x1,
                                base_y + y1 * 31 + y1,
                                base_x + (x1 + 1) * 31 + x1,
                                base_y + (y1 + 1) *31 + y1, 
                                fill=random.choice(COLORES), outline="white", width=1.5)    

def dibujar_casilla(x, y, color):
    """Dibuja una casilla en las coordenadas x , y del color que se indique"""
    gamelib.draw_rectangle(base_x + x * 31 + x, 
                           base_y + y * 31 + y, 
                           base_x + (x + 1) * 31 + x, 
                           base_y + (y + 1) * 31 + y, 
                           fill=color, outline="black", width=1.5)
    gamelib.draw_rectangle(ANCHO//1.548, ALTO// 6.5, ANCHO // 1.34051, ALTO// 6.53,fill="black")
    gamelib.draw_rectangle(ANCHO//1.548, ALTO// 1.47, ANCHO // 1.34051, ALTO// 1.472, fill="black")
    gamelib.draw_rectangle(ANCHO//1.548, ALTO// 6.5, ANCHO // 1.546, ALTO// 1.47, fill="black")
    gamelib.draw_rectangle(ANCHO//1.34049, ALTO// 6.5, ANCHO // 1.34051, ALTO// 1.47, fill="black")

def dibujar_siguiente_pieza(siguiente_pieza, color_pieza_siguiente, modo):
    """Dibuja la siguiente pieza a la derecha de la grilla"""
    for (x, y) in siguiente_pieza:
        gamelib.draw_rectangle(base_x + 400 + x * 31 + x, 
                               base_y + y * 31 + y, 
                               base_x + 400 + (x + 1) * 31 + x, 
                               base_y + (y + 1) * 31 + y,
                               fill = color_pieza_siguiente, 
                               outline="black", width=1.5)
        
        if modo == 5:
            gamelib.draw_rectangle(base_x + 400 + x * 31 + x, 
                               base_y + y * 31 + y, 
                               base_x + 400 + (x + 1) * 31 + x, 
                               base_y + (y + 1) * 31 + y,
                               fill = random.choice(COLORES), 
                               outline="black", width=1.5)

def dibujar_siguiente_pieza2(siguiente_pieza, color_pieza_siguiente, modo):
    for (x, y) in siguiente_pieza:
        gamelib.draw_rectangle(base_x + 400 + x * 31 + x, 
                                base_y + 150 + y * 31 + y, 
                                base_x + 400 + (x + 1) * 31 + x, 
                                base_y + 150 + (y + 1) * 31 + y,
                                fill = color_pieza_siguiente, 
                                outline="black", width=1.5)
        if modo == 5:
                gamelib.draw_rectangle(base_x + 400 + x * 31 + x, 
                                base_y + 150 + y * 31 + y, 
                                base_x + 400 + (x + 1) * 31 + x, 
                                base_y + 150 + (y + 1) * 31 + y,
                                fill = random.choice(COLORES), 
                                outline="black", width=1.5)

def dibujar_siguiente_pieza3(siguiente_pieza, color_pieza_siguiente, modo):
    for (x, y) in siguiente_pieza:
        gamelib.draw_rectangle(base_x + 400 + x * 31 + x, 
                               base_y + 300 + y * 31 + y, 
                               base_x + 400 + (x + 1) * 31 + x, 
                               base_y + 300 + (y + 1) * 31 + y,
                               fill = color_pieza_siguiente, 
                               outline="black", width=1.5)
        
        if modo == 5:
                gamelib.draw_rectangle(base_x + 400 + x * 31 + x, 
                                base_y + 300 + y * 31 + y, 
                                base_x + 400 + (x + 1) * 31 + x, 
                                base_y + 300 + (y + 1) * 31 + y,
                                fill = random.choice(COLORES), 
                                outline="black", width=1.5)
        
    
def dibujar_nuevo_estado_juego(juego, cambiar_pieza, siguiente_pieza, pieza_fantasma, color_pieza, color_pieza_consolidada, color_pieza_siguiente, modo, pieza_futura, pieza_futura2):
    """Recibe un nuevo estado de juego y dibuja la nueva pieza, cambiando la pieza actual por la siguiente 
    si hay que cambiarla, devuelve la pieza modificada y la siguiente pieza"""

    #Dibuja la grilla, piezas consolidadas, la siguiente pieza y la pieza fantasma
    if modo != 7:
        dibujar_piezas_consolidadas(juego, color_pieza_consolidada, modo) 
    dibujar_siguiente_pieza(siguiente_pieza, color_pieza_siguiente, modo)
    dibujar_siguiente_pieza2(pieza_futura, color_pieza_siguiente, modo)
    dibujar_siguiente_pieza3(pieza_futura2, color_pieza_siguiente, modo)
    
    if pieza_fantasma == 1:
         dibujar_pieza_fantasma(juego, modo)     

        #Dibuja la pieza actual
    if modo != 6:
        pieza = pieza_actual(juego)
        for (x, y) in pieza:
            dibujar_casilla(x, y, color_pieza)
            if modo == 5:
                dibujar_casilla(x, y, random.choice(COLORES))
        
    #Si hay que cambiar la pieza la cambia y genera una nueva pieza siguiente
    if cambiar_pieza:

        siguiente_pieza = pieza_futura
        pieza_futura = pieza_futura2
        pieza_futura2 = generar_pieza()  

    
    #Devuelve la siguiente pieza actualizada
    return siguiente_pieza, pieza_futura, pieza_futura2

def dibujar_piezas_consolidadas(juego, color_pieza_consolidada, modo):
    """Dibuja las piezas ya consolidadas"""
    for y in range(len(juego[0])):
        for x in range(len(juego[0][0])): 
            if juego[0][y][x]==2:    
                dibujar_casilla(x, y, color_pieza_consolidada) 
                if modo == 5:
                    dibujar_casilla(x, y, random.choice(COLORES)) 
            
    

def dibujar_grilla_y_controles(puntaje,intervalo, modo, imagen, color, color_es, idioma, color_guia):
    """Genera la grilla del tetris y las instrucciones de los controles"""
    modos_normales = (1,2,3,5,6,7,8,11,12)
    txt_score = traducciones["score"]
    txt_intervalo = traducciones["intervalo"]
    if modo in modos_normales:
        if color_es == True:
            gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill=color)
        else:
            gamelib.draw_image(imagen,-100,-100)
        gamelib.draw_text(f"{txt_score}: {puntaje}    {txt_intervalo}: {intervalo:.3f}",  ANCHO // 208, ALTO // 38.7, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["rotar"], ANCHO // 208, ALTO // 2, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["bajar"], ANCHO // 208, ALTO // 1.85, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["izquierda"], ANCHO // 208, ALTO // 1.73, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["derecha"], ANCHO // 208, ALTO // 1.62, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["espacio"], ANCHO // 208, ALTO // 1.529, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["pause"], ANCHO // 208, ALTO // 1.445, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["esc"], ANCHO // 208, ALTO // 1.37, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["nuevo"], ANCHO // 208, ALTO // 1.30123 , fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["guardarJuego"], ANCHO // 208, ALTO // 1.24, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["cargarJuego"], ANCHO // 208, ALTO // 1.17654, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))

    if modo == 4:
        if color_es == True:
            gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill=color)
        else:
            gamelib.draw_image(imagen,0,-10)
        gamelib.draw_text(f"{txt_score}: {puntaje}    {txt_intervalo}: {intervalo:.3f}",  ANCHO // 208, ALTO // 38.7, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["inv_bajar"], ANCHO // 208, ALTO // 2, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["inv_rotar"], ANCHO // 208, ALTO // 1.85, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["inv_izquierda"], ANCHO // 208, ALTO // 1.73, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["inv_derecha"], ANCHO // 208, ALTO // 1.62, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["inv_espacio"], ANCHO // 208, ALTO // 1.529, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["pause"], ANCHO // 208, ALTO // 1.445, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["esc"], ANCHO // 208, ALTO // 1.37, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["nuevo"], ANCHO // 208, ALTO // 1.30123 , fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["guardarJuego"], ANCHO // 208, ALTO // 1.24, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
        gamelib.draw_text(traducciones["cargarJuego"], ANCHO // 208, ALTO // 1.17654, fill=color_guia, anchor="w", size=int(ALTO * 0.02567))
    gamelib.draw_line(base_x,base_y,
                      base_x,
                      base_y+dimensiones_bloques_px*ALTO_JUEGO,
                      fill=color_guia,width=1)
    
    gamelib.draw_line(base_x+dimensiones_bloques_px*ANCHO_JUEGO,base_y,
                base_x+dimensiones_bloques_px*ANCHO_JUEGO,
                base_y+dimensiones_bloques_px*ALTO_JUEGO,
                fill=color_guia,width=1)
    
    gamelib.draw_line(base_x,base_y+dimensiones_bloques_px*ALTO_JUEGO,
                base_x+dimensiones_bloques_px*ANCHO_JUEGO,
                base_y+dimensiones_bloques_px*ALTO_JUEGO,
                fill=color_guia,width=1)
    #Dibujar Grilla
    for i in range(1, 9):
        gamelib.draw_line(base_x+dimensiones_bloques_px*i,
                          base_y,base_x+dimensiones_bloques_px*i,
                          base_y+(dimensiones_bloques_px*ALTO_JUEGO), 
                          fill=color_guia, width=1)
    for j in range(1, 18):
        gamelib.draw_line(base_x,base_y+dimensiones_bloques_px*j,
                          base_x + (dimensiones_bloques_px*ANCHO_JUEGO),
                          base_y+dimensiones_bloques_px*j, 
                          fill=color_guia, width=1,)

# ---------------------------------------------------------------
# FUNCIONES ESTADO
# ---------------------------------------------------------------

def avanzar_estado_juego(juego, siguiente_pieza,puntaje,intervalo):
    """Avanza al siguiente estado de juego"""

    #Avanza el estado de juego
    juego, cambiar_pieza,cant_filas_elim=avanzar(juego, siguiente_pieza)
    
    puntaje,intervalo=SistemaDePuntaje(cant_filas_elim,puntaje,intervalo)
    #Devuelve el nuevo estado de juego
    return juego,cambiar_pieza, puntaje,intervalo

def SistemaDePuntaje(cant_filas,puntaje,intervalo):
    """Por cada cantidad de filas eliminadas se va acumulando el puntaje que luego es mostrado por pantalla"""    
    puntaje+=int((cant_filas**2)*1000)
    intervalo+=(0.005*(cant_filas**1.5))
    
    return puntaje, intervalo


# ---------------------------------------------------------------
# VENTANAS EXTRA
# ---------------------------------------------------------------      
def pantalla_modos_de_juego(sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol,b, color_pieza,predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente):
    crear_ventana2()
    modo = 0 
    tiempo_total = 0
    while gamelib.loop():
        gamelib.draw_begin()
        gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill="#07051A")
        gamelib.draw_image("imagenes/JUEGO/inicio_juego.ppm",ANCHO//7.678, ALTO//50)
        gamelib.draw_rectangle(ANCHO//3, ALTO//4.425 , ANCHO//77 , ALTO//8.947, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//3, ALTO//2.623 , ANCHO//77 , ALTO//3.7476, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//3, ALTO//1.87 , ANCHO//77 , ALTO//2.3876, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//3, ALTO//1.45 , ANCHO//77 , ALTO//1.7435, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.6485, ALTO//1.35521, ANCHO//77, ALTO//1.0621, fill="#8C2B34", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.5485, ALTO//1.195, ANCHO//1.0186, ALTO//1.0621, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.5485, ALTO//1.24, ANCHO//1.0186, ALTO//1.42, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.445, ALTO//4.425 , ANCHO//2.7 , ALTO//8.947, fill= "#0D1B2A", outline= "#FF00FF") # empieza segunda fila
        gamelib.draw_rectangle(ANCHO//1.445, ALTO//2.623 , ANCHO//2.7 , ALTO//3.7476, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.445, ALTO//1.87 , ANCHO//2.7 , ALTO//2.3876, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.445, ALTO//1.45 , ANCHO//2.7 , ALTO//1.7435, fill= "#0D1B2A", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.015, ALTO//4.425 , ANCHO//1.425 , ALTO//8.947, fill = "#0D1B2A", outline= "#FF00FF") #filas opciones extras
        gamelib.draw_rectangle(ANCHO//1.015, ALTO//3.623 , ANCHO//1.425 , ALTO//3.7476, fill="#00E5FF", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.418, ALTO//1.45 , ANCHO//1.4256 , ALTO//3.7476, fill="#00E5FF", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.015, ALTO//1.45 , ANCHO//1.0186 , ALTO//3.7476, fill="#00E5FF", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.015, ALTO//1.45 , ANCHO//1.425 , ALTO//1.46845, fill="#00E5FF", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.4015, ALTO//1.48 , ANCHO//1.0286 , ALTO//1.7476, fill="#00E5FF", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.4015, ALTO//1.88 , ANCHO//1.0286 , ALTO//2.3476, fill="#00E5FF", outline= "#FF00FF")
        gamelib.draw_rectangle(ANCHO//1.4015, ALTO//2.60 , ANCHO//1.0286 , ALTO//3.54, fill="#00E5FF", outline= "#FF00FF")
       
        gamelib.draw_text(traducciones["modo_normal"], ANCHO//5.65, ALTO//5.923, fill="#39FF14", bold= True, size=int(ALTO * 0.07567))
        gamelib.draw_text(traducciones["modo_rapido"], ANCHO//5.65, ALTO//3.0623, fill="#39FF14", bold= True, size=int(ALTO * 0.07567))
        gamelib.draw_text(traducciones["modo_lento"], ANCHO//5.65, ALTO//2.09, fill="#39FF14", bold= True, size=int(ALTO * 0.07567))
        gamelib.draw_text(traducciones["modo_invertido"], ANCHO//5.65, ALTO//1.576546, fill="#39FF14", bold= True, size=int(ALTO * 0.06867))
        gamelib.draw_text(traducciones["volver_menu"] + " \n", ANCHO//3.17, ALTO//1.142, fill="#39FF14", size=int(ALTO * 0.05967), anchor= "center")
        gamelib.draw_text(traducciones["practica_contrarreloj"], ANCHO//1.23, ALTO//1.322, fill="#39FF14", size=int(ALTO * 0.04767), anchor= "center")
        gamelib.draw_text(traducciones["modo_practica"], ANCHO//1.23, ALTO//1.132, fill="#39FF14", size=int(ALTO * 0.05267), anchor= "center")
        gamelib.draw_text(traducciones["modo_arcoiris"], ANCHO //1.8723, ALTO//5.923, fill="#39FF14", bold= True, size=int(ALTO * 0.07467))
        gamelib.draw_text(traducciones["modo_sin_pieza"], ANCHO //1.8723, ALTO//3.0623, fill="#39FF14", bold= True, size=int(ALTO * 0.06867))
        gamelib.draw_text(traducciones["modo_sin_consolidada"], ANCHO //1.8723, ALTO//2.09, fill="#39FF14", bold= True, size=int(ALTO * 0.047567))
        gamelib.draw_text(traducciones["modo_contrarreloj"], ANCHO //1.8723, ALTO//1.576546, fill="#39FF14", bold= True, size=int(ALTO * 0.0507))
        gamelib.draw_text(traducciones["modo_extras"], ANCHO //1.1823, ALTO//5.923, fill="#39FF14", bold= True, size=int(ALTO * 0.07567))
        for event in gamelib.get_events():
                    if event.type == gamelib.EventType.ButtonPress:
                        x,y = event.x,event.y
                        if event.mouse_button == 1:
                            if x<=ANCHO//3 and x>=ANCHO//77 and y<=ALTO//4.425 and y>=ALTO//8.947:
                                modo = 1
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//3 and x>=ANCHO//77 and y<=ALTO//2.623 and y>=ALTO//3.7476:
                                modo = 2
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//3 and x>=ANCHO//77 and y<=ALTO//1.87 and y>=ALTO//2.3876:
                                modo = 3
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//3 and x>=ANCHO//77 and y<=ALTO//1.45 and y>=ALTO//1.7435:
                                modo = 4
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//1.445 and x>=ANCHO//2.7 and y<=ALTO//4.425 and y>=ALTO//8.947:
                                modo = 5
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//1.445 and x>=ANCHO//2.7 and y<=ALTO//2.623 and y>=ALTO//3.7476:
                                modo = 6
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//1.445 and x>=ANCHO//2.7 and y<=ALTO//1.87 and y>=ALTO//2.3876:
                                modo = 7
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//1.445 and x>=ANCHO//2.7 and y<=ALTO//1.45 and y>=ALTO//1.7435:
                                modo = 8
                                tiempo_total= 30
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//1.0186 and x>=ANCHO//1.5485  and y<=ALTO//1.0621 and y>=ALTO//1.195:
                                modo = 11
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)
                            if x<=ANCHO//1.0186 and x>=ANCHO//1.5485  and y<=ALTO//1.24 and y>=ALTO//1.42:
                                modo = 12
                                tiempo_total_input = gamelib.input("Ingrese el tiempo en segundos:")
                                try:
                                    tiempo_total = int(tiempo_total_input)
                                except:
                                    tiempo_total = 60
                                game_start(on, vol,b)
                                time.sleep(2)
                                jugar(modo,sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente, tiempo_total)    
                            if x<=ANCHO//1.6485 and x>=ANCHO//77 and y<=ALTO//1.0621 and y>=ALTO//1.35521:
                                return
                    if event.type == gamelib.EventType.KeyPress:
                        if event.key == "Escape":
                            return  
    gamelib.draw_end()
    
    return modo

def pantalla_perdiste(puntaje, idioma, modo):
    "Dibuja una ventana que cuando perdes (osea ya no se pueden colocar mas piezas), te muestra que perdiste, tu puntaje y tu lugar en  el ranking y te da la opcion de empezar un nuevo juego, salir al menu principal o salir del juego"
    
    gamelib.draw_rectangle(0,0,ANCHO,ALTO,fill="gray")
    gamelib.draw_text(traducciones["perdiste_titulo"],ANCHO//2,ALTO//2-30,fill="red",size="40")
    gamelib.draw_text(traducciones["perdiste_nuevo"],ANCHO//2,ALTO//2+20,fill="white",size="35")
    if modo != 12:
      gamelib.draw_text(traducciones["perdiste_ranking"],ANCHO//2,ALTO//2+70,fill="white",size="20")
    puntaje_txt = traducciones["perdiste_puntaje"]
    gamelib.draw_text(f"{puntaje_txt}: {puntaje}", ANCHO // 2, ALTO // 1.2, fill="white", size=30, anchor="center")

def game_start(on, vol, b):
    if b == 0: 
       pass
    else:
        if on == 1:
            pygame.mixer.init()
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sonido/game_start.mp3")
            pygame.mixer.music.set_volume(vol)
            pygame.mixer.music.play(-1)
        if on == 0:
            pygame.mixer.music.stop()



def elecciones(imagen, color, color_es, predeterminada, idioma):
    
    crear_ventana2()
    predeterminada= True
    while gamelib.loop():
        gamelib.draw_begin()
        gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill="#07051A")
        gamelib.draw_image("imagenes/JUEGO/inicio_juego.ppm",ANCHO//7.678, ALTO//50)
        gamelib.draw_rectangle(ANCHO//77,ALTO//2.25,ANCHO//3.2,ALTO//77, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//2.9,ALTO//2.25,ANCHO//1.545,ALTO//77, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.4726,ALTO//2.25,ANCHO//1.0235,ALTO//77, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.6485, ALTO//1.35521, ANCHO//77, ALTO//1.0621, fill="#8C2B34", outline="#0A0A23")
        
        
        gamelib.draw_text(traducciones["fondo_predeterminado"], ANCHO// 6.15, ALTO// 4.53, fill ="#E2E2E2", size=int(ALTO * 0.02527), bold = True, anchor="center")
        gamelib.draw_text(traducciones["fondo_personalizado"], ANCHO// 2.05, ALTO// 4.53, fill ="#E2E2E2", size=int(ALTO * 0.02527), bold = True, anchor="center")
        gamelib.draw_text(traducciones["fondo_color"], ANCHO// 1.22, ALTO// 4.53, fill ="#E2E2E2", size=int(ALTO * 0.02527), bold = True, anchor="center")
        gamelib.draw_text(traducciones["volver_menu"] + " \n", ANCHO//3.17, ALTO//1.142, fill="#E2E2E2", size=int(ALTO * 0.05967), anchor= "center")
        for event in gamelib.get_events():
                    if event.type == gamelib.EventType.ButtonPress:
                        x,y = event.x,event.y
                        if event.mouse_button == 1:
                            if x>= ANCHO//77 and x<= ANCHO//3.2 and y>=ALTO//77 and y<=ALTO//2.25:
                                predeterminada = True
                                imagen, color_es, predeterminada = elegir_imagen_fondo(imagen, color_es, predeterminada)
                            if x>= ANCHO//2.9 and x<= ANCHO//1.545 and y>=ALTO//77 and y<=ALTO//2.25:
                                predeterminada = False 
                                imagen, color_es, predeterminada = elegir_imagen_fondo(imagen, color_es, predeterminada) 
                            if x>= ANCHO//1.4726 and x<= ANCHO//1.0235 and y>=ALTO//77 and y<=ALTO//2.25:
                                color, color_es = elegir_color_fondo(color, color_es)
                            if x<=ANCHO//1.6485 and x>=ANCHO//77 and y<=ALTO//1.0621 and y>=ALTO//1.35521:
                                return imagen, color, color_es, predeterminada, idioma
                            
    gamelib.draw_end()
           
    return imagen, color, color_es, predeterminada, idioma

def colores(color_pieza, color_pieza_consolidada, color_guia, color_pieza_siguiente, idioma):
    
    crear_ventana2()
    predeterminada= True
    while gamelib.loop():
        gamelib.draw_begin()
        gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill="#07051A")
        gamelib.draw_image("imagenes/JUEGO/inicio_juego.ppm",ANCHO//7.678, ALTO//50)
        gamelib.draw_rectangle(ANCHO//77,ALTO//2.25,ANCHO//3.2,ALTO//77, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//2.9,ALTO//2.25,ANCHO//1.545,ALTO//77, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.4726,ALTO//2.25,ANCHO//1.0235,ALTO//77, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.4726,ALTO//2,ANCHO//1.0235,ALTO//1.0621, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.6485, ALTO//1.35521, ANCHO//77, ALTO//1.0621, fill="#8C2B34", outline="#0A0A23")
        
        gamelib.draw_text(traducciones["volver_menu"] + " \n", ANCHO//3.17, ALTO//1.142, fill="#E2E2E2", size=int(ALTO * 0.05967), anchor= "center")
        gamelib.draw_text(traducciones["color_pieza"], ANCHO// 6.15, ALTO// 4.53, fill ="#E2E2E2", size=int(ALTO * 0.03627), bold = True, anchor="center")
        gamelib.draw_text(traducciones["color_pieza_fija"], ANCHO// 2.05, ALTO// 4.53, fill ="#E2E2E2", size=int(ALTO * 0.03227), bold = True, anchor="center")
        gamelib.draw_text(traducciones["color_guia_texto"], ANCHO// 1.22, ALTO// 4.53, fill ="#E2E2E2", size=int(ALTO * 0.03227), bold = True, anchor="center")
        gamelib.draw_text(traducciones["color_pieza_siguiente_texto"], ANCHO// 1.20, ALTO// 1.4023, fill ="#E2E2E2", size=int(ALTO * 0.03587), bold = True, anchor="center")
        for event in gamelib.get_events():
                    if event.type == gamelib.EventType.ButtonPress:
                        x,y = event.x,event.y
                        if event.mouse_button == 1:
                            if x>= ANCHO//77 and x<= ANCHO//3.2 and y>=ALTO//77 and y<=ALTO//2.25:
                                color_pieza = elegir_color_pieza(color_pieza)
                            if x>= ANCHO//2.9 and x<= ANCHO//1.545 and y>=ALTO//77 and y<=ALTO//2.25:
                                color_pieza_consolidada = elegir_color_pieza(color_pieza_consolidada)
                            if x>= ANCHO//1.4726 and x<= ANCHO//1.0235 and y>=ALTO//77 and y<=ALTO//2.25:
                                color_guia = elegir_color_pieza(color_guia)
                            if x>= ANCHO//1.4726 and x<= ANCHO//1.0235 and y>=ALTO//2 and y<=ALTO//1.0621:
                                color_pieza_siguiente = elegir_color_pieza(color_pieza_siguiente)
                            if x<=ANCHO//1.6485 and x>=ANCHO//77 and y<=ALTO//1.0621 and y>=ALTO//1.35521:
                                return color_pieza, color_pieza_consolidada, color_guia, color_pieza_siguiente
                            
    gamelib.draw_end()
           
    return color_pieza, color_pieza_consolidada, color_guia, color_pieza_siguiente

def inicio_juego():
    """Crea una ventana aparte que es el incio del juego, en esta podes elegir distintos modos, configuración, accesibilidad y creditos"""
    
    crear_ventana2()
    on= 1
    pieza_fantasma = 1
    vol = 0.1
    sonido="sonido/tetris1.mp3"
    imagen="imagenes/predeterminadas/imagen2.ppm"
    idioma=1
    color= ""
    color_es = False

    b = 1
    predeterminada = True
    color_pieza = "#519CB9"
    color_pieza_consolidada=  "#11506B"
    color_guia = "white"
    color_pieza_siguiente = "white"
    if on== 1:
        pygame.mixer.init()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sonido\inicio.mp3")
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)
    if on== 0:
         pygame.mixer.music.stop()
    while gamelib.loop():
        gamelib.draw_begin()
        gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill="#07051A")
        gamelib.draw_image("imagenes/JUEGO/inicio_juego.ppm",ANCHO//7.678, ALTO//50)
        gamelib.draw_rectangle(ANCHO//1.45843 + ANCHO//592.9, ALTO//3.15 + ALTO//11, ANCHO//2 - ANCHO // 5.3756, ALTO//3.15 - ALTO//52, fill="#E41313", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.45843 + ANCHO//592.9, ALTO//2 + ALTO//11 , ANCHO//2 - ANCHO // 5.3756, ALTO//2 - ALTO//52, fill="#AE830B", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.45843 + ANCHO//592.9, ALTO//1.45 + ALTO//11, ANCHO//2 - ANCHO // 5.3756, ALTO//1.45 - ALTO//52, fill="#1B0BB3", outline="#0A0A23")

        
        gamelib.draw_text(traducciones["tetris"],ANCHO//2, ALTO // 6, fill="#ECDFB5", size=120)
        gamelib.draw_text(traducciones["jugar"],ANCHO//2, ALTO // 2.8124, fill="#E2E2E2", bold= True, size=int(ALTO * 0.06667))
        gamelib.draw_text(traducciones["config"],ANCHO//2, ALTO // 1.8678, fill="#E2E2E2", bold= True, size=int(ALTO * 0.05867))
        gamelib.draw_text(traducciones["salir1"],ANCHO//2, ALTO // 1.3724, fill="#E2E2E2", bold= True, size=int(ALTO * 0.06667))
        
        for event in gamelib.get_events():
                    if event.type == gamelib.EventType.ButtonPress:
                        x,y = event.x,event.y
                        if event.mouse_button == 1:
                            if x<=ANCHO//1.45843 + ANCHO//592.9 and x>=ANCHO//2 - ANCHO // 5.3756 and y<=ALTO//3.15 + ALTO//11 and y>=ALTO//3.15 - ALTO//52:
                                pantalla_modos_de_juego(sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente)  
                            if x<=ANCHO//1.45843 + ANCHO//592.9 and x>=ANCHO//2 - ANCHO // 5.3756 and y<=ALTO//2 + ALTO//11 and y>=ALTO//2 - ALTO//52:
                                sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente = configuracion(sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente)
                                if color_pieza == None:
                                   color_pieza= "#519CB9"
                                if color_pieza_consolidada== None:
                                   color_pieza_consolidada= "#11506B"
                                if color_guia == None:
                                    color_guia = "white"
                                if color_pieza_siguiente == None:
                                    color_pieza_siguiente = "white"
                            if x<=ANCHO//1.45843 + ANCHO//592.9 and x>=ANCHO//2 - ANCHO // 5.3756 and y<=ALTO//1.45 + ALTO//11 and y>=ALTO//1.45 - ALTO//52:
                                return 1
        gamelib.draw_end()
# ---------------------------------------------------------------
# CONFIGURACION DE ANCHO, ALTO Y VENTANA
# ---------------------------------------------------------------
                
def crear_ventana(sonido, on, vol):
    """Crea la ventana obteniendo el alto y ancho del monitor del usuario"""
    
    gamelib.resize(ANCHO, ALTO)
    gamelib.title("TETRIS")
    if on == 1:
        pygame.mixer.init()
        pygame.mixer.music.stop()
        print(sonido)
        pygame.mixer.music.load(sonido)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)
    if on == 0:
        pygame.mixer.music.stop()
    

def crear_ventana2():
    """Crea la ventana obteniendo el alto y ancho del monitor del usuario"""
    
    gamelib.resize(ANCHO, ALTO)

def obtener_ancho_alto():
        """Obtiene el ancho y alto del monitor del usuario y lo devuelve"""
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()

        ANCHO = root.winfo_screenwidth()
        ALTO = root.winfo_screenheight()

        root.destroy()

        return ANCHO, ALTO


# ---------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------

def configuracion(sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente):
    
    crear_ventana2()
    ju = 0
    nashei= 0
    while gamelib.loop():
        gamelib.draw_begin()
        gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill="#07051A")
        gamelib.draw_image("imagenes/JUEGO/inicio_juego.ppm",ANCHO//7.678, ALTO//50)
        gamelib.draw_rectangle(ANCHO//3.3323, ALTO//4.425 , ANCHO//77 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.13, ALTO//4.425 , ANCHO//1.6485 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")  
        gamelib.draw_rectangle(ANCHO//1.60134, ALTO//4.425 , ANCHO//1.0985 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.3323, ALTO//3.9425 , ANCHO//77 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.13, ALTO//3.9425 , ANCHO//1.6485 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.60134, ALTO//3.9425 , ANCHO//1.0985 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.3323, ALTO//2.01521 , ANCHO//77 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.13, ALTO//2.01521 , ANCHO//1.6485 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.60134, ALTO//2.01521 , ANCHO//1.0985 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.60134, ALTO//1.35521 , ANCHO//1.0985 , ALTO//1.0621, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.091, ALTO//1.0621, ANCHO//1.00632, ALTO//77, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.6485, ALTO//1.35521, ANCHO//77, ALTO//1.0621, fill="#8C2B34", outline="#0A0A23")

        gamelib.draw_text(traducciones["silenciar"], ANCHO//77, ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.05367), anchor= "w")
        gamelib.draw_text(traducciones["volumen"], ANCHO//3.10, ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.05367), anchor= "w")
        gamelib.draw_text(traducciones["musica_personalizada"], ANCHO//1.591, ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.04767), anchor= "w")
        gamelib.draw_text(traducciones["mostrar_fantasma"], ANCHO//53, ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.04867), anchor= "w")
        gamelib.draw_text(traducciones["cambiar_colores"], ANCHO//3.10, ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.04667), anchor= "w")
        gamelib.draw_text(traducciones["ayuda"], ANCHO//1.591, ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.06067), anchor= "w")
        gamelib.draw_text(traducciones["ver_creditos"], ANCHO//53, ALTO// 1.74, fill="#E2E2E2", size=int(ALTO * 0.04967), anchor= "w")
        gamelib.draw_text(traducciones["elegir_musica"], ANCHO//1.591, ALTO// 1.74, fill="#E2E2E2", size=int(ALTO * 0.04967), anchor= "w")
        gamelib.draw_text(traducciones["elegir_contenido"], ANCHO//3.10, ALTO// 1.74, fill="#E2E2E2", size=int(ALTO * 0.05037), anchor= "w")
        gamelib.draw_text(traducciones["cambiar_idioma"], ANCHO//1.581, ALTO// 1.198, fill="#E2E2E2", size=int(ALTO * 0.05467), anchor= "w")
        gamelib.draw_text("C\nO\nN\nF\n I\nG\nU\nR\nA\nC\n I\nO\nN\n \nY\n ", ANCHO//1.05832, ALTO// 2, fill="#E2E2E2", size=int(ALTO * 0.03654), anchor= "center")
        gamelib.draw_text("A\nC\nE\nS\nS\n I\nB\n I\nL\n I\nD\nA\nD\n \ \n❤",ANCHO//1.02632, ALTO// 2, fill="#E2E2E2", size=int(ALTO * 0.03654), anchor= "center")
        gamelib.draw_text(traducciones["volver_menu"] + " \n", ANCHO//3.17, ALTO//1.142, fill="#E2E2E2", size=int(ALTO * 0.05967), anchor= "center")

        for event in gamelib.get_events():
                    if event.type == gamelib.EventType.ButtonPress:
                        x,y = event.x,event.y
                        if event.mouse_button == 1:
                            if x<=ANCHO//3.3323 and x>=ANCHO//77 and y<=ALTO//4.425 and y>=ALTO//75.947:
                                on = silenciar_musica(on, vol, b)
                            if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y<=ALTO//4.425 and y>=ALTO//75.947:
                                vol = volumen_de_musica(vol, on, b)
                            if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y<=ALTO//4.425 and y>=ALTO//75.947:
                                sonido = elegir_sonido_personalizado(sonido)
                            if x<=ANCHO//3.3323 and x>=ANCHO//77 and y>=ALTO//3.9425 and y<=ALTO//2.147:
                                pieza_fantasma = mostrar_pieza_fantasma(pieza_fantasma)
                            if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y>=ALTO//3.9425 and y<=ALTO//2.147:
                                while ju == 0:
                                    gamelib.say("Este modo es más avanzado en terminos graficos y queda totalmente a gusto del usuario (este mensaje solo aparecera una vez)")
                                    ju += 1
                                color_pieza, color_pieza_consolidada, color_guia, color_pieza_siguiente = colores(color_pieza, color_pieza_consolidada, color_guia, color_pieza_siguiente, idioma)
                            if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>=ALTO//3.9425 and y<=ALTO//2.147:                                                                                                                                             
                                abrir_pdf("TETRIS DEX.pdf")
                            
                            if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y>=ALTO//2.01521 and y<=ALTO//1.41:
                                if b == 0:
                                    gamelib.say("AL ESTAR EN EL IDIOMA ANGRY BIRDS NO SE PUEDE ELEGIR FONDO NI MUSICA. PARA PODER ELEGIR APRETE EL IDIOMA ESPAÑOL DE VUELTA")
                                else:    
                                    imagen, color, color_es, predeterminada, idioma = elecciones(imagen, color, color_es, predeterminada, idioma)
                            if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>=ALTO//2.01521 and y<=ALTO//1.41:
                                if b == 0:
                                    gamelib.say("AL ESTAR EN EL IDIOMA ANGRY BIRDS NO SE PUEDE ELEGIR FONDO NI MUSICA. PARA PODER ELEGIR APRETE EL IDIOMA ESPAÑOL DE VUELTA")
                                else:
                                    sonido = sonido_a_elegir(sonido, idioma, on, vol)
                            if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>= ALTO//1.35521 and y<=ALTO//1.0621:
                                idioma , sonido, color, color_es, imagen, b= idiomas(idioma, sonido, color, color_es, imagen, b)
                            if x<=ANCHO//1.6485 and x>=ANCHO//77 and y>=ALTO//1.35521 and y<=ALTO//1.0621:
                                return sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente

    gamelib.draw_end()

    return sonido, imagen, color, color_es, idioma, on, pieza_fantasma, vol, b, color_pieza, predeterminada, color_pieza_consolidada, color_guia, color_pieza_siguiente

def silenciar_musica(on, vol, b):
    if b == 0:
        gamelib.say("NO SE PUEDE APAGAR LA MUSICA POR TEMAS DEL IDIOMA ANGRY BIRDS. PARA PODER SILENCIAR LA MUSICA Y HACER QUE TODO VUELVA A LA NORMALIDAD VAYA AL IDIOMA ESPAÑOL")
    if on == 1 and b == 1:
        pygame.mixer.music.stop()
        on = 0
        return on
    if on == 0 and b == 1:
        pygame.mixer.init()
        pygame.mixer.music.load("sonido/inicio.mp3")
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)
        on = 1
        return on 

def volumen_de_musica(vol, on, b):
    if b == 0:
        gamelib.say("NO SE PUEDE AJUSTAR EL VOLUMEN DE MUSICA POR TEMAS DEL IDIOMA ANGRY BIRDS. PARA PODER AJUSTAR EL VOLUMEN DE LA MUSICA Y HACER QUE TODO VUELVA A LA NORMALIDAD VAYA AL IDIOMA ESPAÑOL")
    if on == 1 and b == 1:
        while True:
            vol = gamelib.input("Ingrese el volumen (desde el 0.0 hasta el 1.0, ej: 0.5 es la mitad):")

            if vol is None or vol == "":
                print("Operación cancelada. Se mantiene el volumen actual.")
                return None
            
            try:
                vol = float(vol)
            except ValueError:
                gamelib.say("Error: Ingrese un número válido (ej: 0.75).")
                continue 

            if 0.0 <= vol <= 1.0:
                pygame.mixer.init()
                pygame.mixer.music.load("sonido/inicio.mp3")
                pygame.mixer.music.set_volume(vol)
                pygame.mixer.music.play(-1)
                return vol
            else:
                gamelib.say("Error: El volumen debe estar entre 0.0 y 1.0 (ambos inclusive).")
    if on == 0:
        gamelib.say("Active el volumen primero para poder escuchar")
        return vol
    
def mostrar_pieza_fantasma(pieza_fantasma):
    if pieza_fantasma == 1:
        pieza_fantasma = 0
        gamelib.say("Pieza fantasma desactivada.")
        return pieza_fantasma
    if pieza_fantasma == 0:
        pieza_fantasma = 1
        gamelib.say("Pieza fantasma activada.")
        return pieza_fantasma

def abrir_pdf(ruta):
    if platform.system() == "Windows":     
        os.startfile(ruta)
    elif platform.system() == "Darwin":     
        os.system(f"open '{ruta}'")
    else:                                
        os.system(f"xdg-open '{ruta}'")

def sonido_a_elegir(sonido, idioma, on, vol):
    gamelib.draw_begin()
    crear_ventana2()
    gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill="#07051A")
    gamelib.draw_image("imagenes/JUEGO/inicio_juego.ppm",ANCHO//7.678, ALTO//50)
    gamelib.draw_rectangle(ANCHO//3.3323, ALTO//4.425 , ANCHO//77 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//3.13, ALTO//4.425 , ANCHO//1.6485 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//1.60134, ALTO//4.425 , ANCHO//1.0985 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//3.3323, ALTO//3.9425 , ANCHO//77 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//3.13, ALTO//3.9425 , ANCHO//1.6485 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//1.60134, ALTO//3.9425 , ANCHO//1.0985 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//3.3323, ALTO//2.01521 , ANCHO//77 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//3.13, ALTO//2.01521 , ANCHO//1.6485 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//1.60134, ALTO//2.01521 , ANCHO//1.0985 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//1.60134, ALTO//1.35521 , ANCHO//1.0985 , ALTO//1.0621, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//1.091, ALTO//1.0621, ANCHO//1.00632, ALTO//77, fill="#3A4F7A", outline="#0A0A23")
    gamelib.draw_rectangle(ANCHO//1.6485, ALTO//1.35521, ANCHO//77, ALTO//1.0621, fill="#8C2B34", outline="#0A0A23")

    _m = traducciones["musica"]
    gamelib.draw_text(_m + " 1", ANCHO//77, ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    gamelib.draw_text(_m + " 2", ANCHO//3.10, ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    gamelib.draw_text(_m + " 3", ANCHO//1.591, ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    gamelib.draw_text(_m + " 4", ANCHO//53, ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    gamelib.draw_text(_m + " 5", ANCHO//3.10, ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    gamelib.draw_text(_m + " 6", ANCHO//1.591, ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    gamelib.draw_text(_m + " 7", ANCHO//53, ALTO// 1.74, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    gamelib.draw_text(_m + " 8", ANCHO//3.10, ALTO// 1.74, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    gamelib.draw_text(_m + " 9", ANCHO//1.591, ALTO// 1.74, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
    _m_vert = "\n".join(_m)
    gamelib.draw_text(_m_vert, ANCHO//1.05832, ALTO// 2.0932, fill="#E2E2E2", size=int(ALTO * 0.02954), anchor= "center")
    gamelib.draw_text(traducciones["parar_musica"], ANCHO//1.581, ALTO// 1.198, fill="#E2E2E2", size=int(ALTO * 0.05367), anchor= "w")
    gamelib.draw_text("❤\n❤\n❤\n❤\n❤", ANCHO//1.02632, ALTO// 2, fill="#E2E2E2", size=int(ALTO * 0.03654), anchor= "center")
    gamelib.draw_text(traducciones["volver_menu"] + " \n", ANCHO//3.17, ALTO//1.142, fill="#E2E2E2", size=int(ALTO * 0.05967), anchor= "center")

    while gamelib.loop():
        for event in gamelib.get_events():
            if event.type == gamelib.EventType.ButtonPress:
                x,y = event.x,event.y
                if event.mouse_button == 1:
                    if x<=ANCHO//3.3323 and x>=ANCHO//77 and y<=ALTO//4.425 and y>=ALTO//75.947:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris1.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris1.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta música porfavor activa el sonido desde la pantalla configuración.")
                    if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y<=ALTO//4.425 and y>=ALTO//75.947:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris2.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris2.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta musica porfavor activa el sonido desde la pantalla configuración.")
                    if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y<=ALTO//4.425 and y>=ALTO//75.947:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris3.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris3.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta musica porfavor activa el sonido desde la pantalla configuración.")
                    if x<=ANCHO//3.3323 and x>=ANCHO//77 and y>=ALTO//3.9425 and y<=ALTO//2.147:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris4.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris4.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta musica porfavor activa el sonido desde la pantalla configuración.")
                    if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y>=ALTO//3.9425 and y<=ALTO//2.147:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris5.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris5.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta musica porfavor activa el sonido desde la pantalla configuración.") 
                    if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>=ALTO//3.9425 and y<=ALTO//2.147:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris6.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris6.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta musica porfavor activa el sonido desde la pantalla configuración.")
                    if x<=ANCHO//3.3323 and x>=ANCHO//77 and y>=ALTO//2.01521 and y<=ALTO//1.41:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris7.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris7.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta musica porfavor activa el sonido desde la pantalla configuración.")
                    if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y>=ALTO//2.01521 and y<=ALTO//1.41:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris8.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris8.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta musica porfavor activa el sonido desde la pantalla configuración.")
                    if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>=ALTO//2.01521 and y<=ALTO//1.41:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/tetris9.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                            sonido= "sonido/tetris9.mp3"
                        if on == 0:
                            gamelib.say("Para poder escuchar esta musica porfavor activa el sonido desde la pantalla configuración.")
                    if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>=ALTO//1.35521 and y<=ALTO//1.0621:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/inicio.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)
                        if on == 0:
                            gamelib.say("La música ya esta parada crack :).")
                    if x<=ANCHO//1.6485 and x>=ANCHO//77 and y>=ALTO//1.35521 and y<=ALTO//1.0621:
                        if on == 1:
                            pygame.mixer.init()
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sonido/inicio.mp3")
                            pygame.mixer.music.set_volume(vol)
                            pygame.mixer.music.play(-1)       
                            return sonido
                        if on == 0:
                            return 
    gamelib.draw_end() 

    return sonido

def idiomas(idioma, sonido, color, color_es, imagen, b):
    global traducciones
    
    crear_ventana2()
    while gamelib.loop():
        gamelib.draw_begin()
        gamelib.draw_rectangle(0,0,ANCHO,ALTO, fill="#07051A")
        gamelib.draw_image("imagenes/JUEGO/inicio_juego.ppm",0,0)
        gamelib.draw_rectangle(ANCHO//3.3323, ALTO//4.425 , ANCHO//77 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.13, ALTO//4.425 , ANCHO//1.6485 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.60134, ALTO//4.425 , ANCHO//1.0985 , ALTO//75.947, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.3323, ALTO//3.9425 , ANCHO//77 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.13, ALTO//3.9425 , ANCHO//1.6485 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.60134, ALTO//3.9425 , ANCHO//1.0985 , ALTO//2.147, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.3323, ALTO//2.01521 , ANCHO//77 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//3.13, ALTO//2.01521 , ANCHO//1.6485 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.60134, ALTO//2.01521 , ANCHO//1.0985 , ALTO//1.41, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.60134, ALTO//1.35521 , ANCHO//1.0985 , ALTO//1.0621, fill="#3A4F7A", outline="#0A0A23")
        gamelib.draw_rectangle(ANCHO//1.6485, ALTO//1.35521, ANCHO//77, ALTO//1.0621, fill="#8C2B34", outline="#0A0A23")
        gamelib.draw_text("Español",ANCHO//77,ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("English",ANCHO//3.10,ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("Français",ANCHO//1.591,ALTO// 11.13232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("Português",ANCHO//53,ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("日本語",ANCHO//3.10,ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("中文",ANCHO//1.591,ALTO// 3.018232, fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("Italiano",ANCHO//53,ALTO// 1.74,fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("Русский",ANCHO//1.591, ALTO// 1.74,fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("Deutsch",ANCHO//3.10,ALTO// 1.74,fill="#E2E2E2", size=int(ALTO * 0.06667), anchor= "w")
        gamelib.draw_text("🐦 Angry Birds", ANCHO//1.581, ALTO// 1.198,   fill="#E2E2E2", size=int(ALTO * 0.05367), anchor= "w")
        gamelib.draw_text(traducciones["volver_menu"] + " \n", ANCHO//3.17, ALTO//1.142, fill="#E2E2E2", size=int(ALTO * 0.05967), anchor= "center")
        for event in gamelib.get_events():
                    if event.type == gamelib.EventType.ButtonPress:
                        x,y = event.x,event.y
                        if event.mouse_button == 1:
                            if x<=ANCHO//3.3323 and x>=ANCHO//77 and y<=ALTO//4.425 and y>=ALTO//75.947:
                                idioma = 1
                                traducciones = cargar_idioma(idioma)
                                if b == 0:
                                    pygame.mixer.music.stop()
                                    pygame.mixer.music.load("sonido/inicio.mp3")
                                    pygame.mixer.music.set_volume(1)
                                    pygame.mixer.music.play(-1) 
                                    imagen = "imagenes/predeterminadas/imagen2.ppm"
                                    sonido = "sonido/tetris.mp3"
                                    color_es= False
                                    b = 1
                                    gamelib.say("Se puso la musica e imagen predeterminada")
                            if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y<=ALTO//4.425 and y>=ALTO//75.947:
                                idioma = 2
                                traducciones = cargar_idioma(idioma)
                            if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y<=ALTO//4.425 and y>=ALTO//75.947:
                                idioma = 3
                                traducciones = cargar_idioma(idioma)
                            if x<=ANCHO//3.3323 and x>=ANCHO//77 and y>=ALTO//3.9425 and y<=ALTO//2.147:
                                idioma = 4
                                traducciones = cargar_idioma(idioma)
                            if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y>=ALTO//3.9425 and y<=ALTO//2.147:
                                idioma = 5
                                traducciones = cargar_idioma(idioma)
                            if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>=ALTO//3.9425 and y<=ALTO//2.147:
                                idioma = 6
                                traducciones = cargar_idioma(idioma)
                            if x<=ANCHO//3.3323 and x>=ANCHO//77 and y>=ALTO//2.01521 and y<=ALTO//1.41:
                                idioma = 7
                                traducciones = cargar_idioma(idioma)
                            if x>=ANCHO//3.13 and x<=ANCHO//1.6485 and y>=ALTO//2.01521 and y<=ALTO//1.41:
                                idioma = 8
                                traducciones = cargar_idioma(idioma)
                            if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>=ALTO//2.01521 and y<=ALTO//1.41:
                                idioma = 9
                                traducciones = cargar_idioma(idioma)
                            if x>=ANCHO//1.60134 and x<=ANCHO//1.0985 and y>= ALTO//1.35521 and y<=ALTO//1.0621: 
                                idioma = 10
                                traducciones = cargar_idioma(idioma)
                                b= 0
                                sonido = "sonido/Angry_Bird.mp3"
                                pygame.mixer.music.load("sonido/aajuñiga.mp3")
                                pygame.mixer.music.set_volume(0.1)
                                pygame.mixer.music.play() 
                                time.sleep(2)
                                pygame.mixer.music.stop() 
                                pygame.mixer.music.load(sonido)
                                pygame.mixer.music.set_volume(0.1)
                                pygame.mixer.music.play(-1)
                                color= "red"
                                color_es= True
                            if x<=ANCHO//1.6485 and x>=ANCHO//77 and y>=ALTO//1.35521 and y<=ALTO//1.0621:
                                return idioma, sonido, color, color_es, imagen, b
                            

    gamelib.draw_end()

    return idioma, sonido, color, color_es, imagen, b

# ---------------------------------------------------------------
# Tkinter
# ---------------------------------------------------------------

def elegir_color_pieza(color_pieza):
    """
    Abre un selector de color real del sistema operativo.
    Devuelve un color en formato "#rrggbb".
    """
    root = tk.Tk()
    root.withdraw()

    color = colorchooser.askcolor(title="Elegir color de la pieza")

    root.destroy()

    return color[1] 

def elegir_color_fondo(color, color_es):
    """
    Selector de color para el FONDO del juego.
    Devuelve:
        color (str): "#rrggbb" o None
        color_es (bool): True si eligió un color, False si canceló
    """
    root = tk.Tk()
    root.withdraw()

    color_select = colorchooser.askcolor(title="Elegir color del fondo")

    root.destroy()

    color = color_select[1]   

    if color is None:
        return None, False    
    else:
        return color, True
       
def elegir_imagen_fondo(imagen_actual, color_es_actual, predeterminada):
    """
    Abre un selector de archivo para elegir una IMAGEN DE FONDO.
    Devuelve:
        imagen (str): ruta de la imagen (o la anterior si canceló)
        color_es (bool): siempre False porque al elegir imagen se desactiva el color
    """
    root = tk.Tk()
    root.withdraw()

    if predeterminada:
        archivo = filedialog.askopenfilename(
            initialdir="imagenes/predeterminadas",
            title="Elegir imagen de fondo",
            filetypes=[("imagenes", "*.png *.jpg *.jpeg *.bmp *.gif *.ppm")]
        )   

    if not predeterminada:
        archivo = filedialog.askopenfilename(
            initialdir="imagenes/personalizadas",
            title="Elegir imagen de fondo",
            filetypes=[("imagenes", "*.png *.jpg *.jpeg *.bmp *.gif *.ppm")]
        )   

    root.destroy()

    if not archivo:
        return imagen_actual, color_es_actual, predeterminada

    return archivo, False, predeterminada

def elegir_sonido_personalizado(sonido_actual):
    """
    Abre un selector de archivo para elegir una IMAGEN DE FONDO.
    Devuelve:
        imagen (str): ruta de la imagen (o la anterior si canceló)
        color_es (bool): siempre False porque al elegir imagen se desactiva el color
    """
    root = tk.Tk()
    root.withdraw()

    archivo = filedialog.askopenfilename(
        initialdir="sonido/personalizadas",
        title="Elegir sonido personalizado",
        filetypes=[("sonido", "*.mp3 *.flac")]
    )   

    root.destroy()

    if not archivo:
        return sonido_actual, 

    return archivo



# ---------------------------------------------------------------
# MEDIDAS UNIVERSALES UWU
# ---------------------------------------------------------------

ANCHO, ALTO = obtener_ancho_alto()
dimensiones_bloques_px=32
base_x = (ANCHO - (dimensiones_bloques_px*ANCHO_JUEGO)) // 2     
base_y = (ALTO - (dimensiones_bloques_px*ALTO_JUEGO)) // 2
traducciones = cargar_idioma(1)

"""traducciones = cargar_idioma(idioma)"""
def iniciar_juego():
    A=0
    while A!=1:
        A=gamelib.init(inicio_juego)
iniciar_juego()

# 25 al 28 se cargan las notas en las planillas de los profes