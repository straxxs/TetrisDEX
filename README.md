# TetrisDEX

Una versión completa del clásico Tetris, desarrollada en Python con tkinter (a través de `gamelib`, incluido en el propio repositorio). Suma varios modos de juego, personalización y guardado de partidas.


## Características Principales

* **Modos de Juego:** normal, rápido, lento, invertido, arcoíris, sin pieza actual, sin pieza consolidada y contrarreloj.
* **Ayudas Visuales:** pieza fantasma y vista de las próximas piezas.
* **Progreso:** sistema de puntuación, ranking por modo y guardado/carga de partidas.
* **Personalización:** colores, sonido y soporte para varios idiomas mediante archivos JSON.


## Requisitos

* Python 3.8 o superior, con `tkinter` (incluido por defecto en Windows y Mac; en algunas distros de Linux hay que instalarlo aparte, por ejemplo `sudo apt install python3-tk`).
* No hace falta instalar ninguna dependencia externa: `gamelib.py` ya está incluido en el repositorio y sólo usa la librería estándar de Python.


## Cómo Ejecutar

1. Cloná o descargá este repositorio.
2. Desde la carpeta `TETRIS FINAL V1.0.0`, ejecutá el archivo principal del juego:

```bash
python main_ejecutable_tetris.py
```

> Conviene correrlo desde esa carpeta para que cargue bien los idiomas y los archivos de texto guardados.


## Controles

* Flechas o WASD: mover y rotar la pieza
* Espacio: bajar hasta el fondo
* P: pausa | N: nuevo juego | G: guardar | C: cargar | Esc: salir
