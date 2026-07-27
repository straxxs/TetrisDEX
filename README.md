# TetrisDEX

TetrisDEX es una versión completa y divertida del clásico juego Tetris, desarrollada en Python. Combina una interfaz visual llamativa, distintos modos de juego, opciones de personalización y varias funciones que hacen la experiencia más completa.

Este proyecto mezcla lógica de juego, gráficos, sonido y manejo de archivos para ofrecer una experiencia más dinámica que una partida tradicional de Tetris.

## Características principales

- Varios modos de juego: normal, rápido, lento, invertido, arcoíris, sin pieza actual, sin pieza consolidada y contrarreloj.
- Una pieza fantasma que ayuda a anticipar dónde caerá la pieza actual.
- Vista de las próximas piezas para planificar mejor los movimientos.
- Un sistema de puntuación que sube según las filas que se eliminan.
- Ranking por modo de juego, guardado en archivos de texto.
- Posibilidad de guardar y cargar partidas.
- Soporte para varios idiomas mediante archivos JSON.
- Opciones para personalizar colores y sonido.
- Un menú interactivo con diferentes pantallas y opciones de juego.

## Requisitos

- Python 3.8 o superior
- pygame

## Instalación

1. Descarga este repositorio o clónalo en tu computadora.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Instala la dependencia necesaria:

```bash
pip install pygame
```

## Ejecución

Desde la carpeta principal del proyecto, ejecuta:

```bash
python main_ejecutable_tetris.py
```

> Es recomendable ejecutar el programa desde la carpeta del proyecto para que se carguen correctamente las imágenes, los sonidos y los archivos de texto.

## Controles

- Flechas o WASD: mover la pieza
- Arriba o W: rotar la pieza
- Abajo o S: bajar la pieza
- Espacio: bajar hasta el fondo
- P: pausar
- N: iniciar un nuevo juego
- G: guardar partida
- C: cargar partida
- Esc: salir

## Estructura del proyecto

- main_ejecutable_tetris.py: punto de entrada principal del juego
- tetris.py: lógica del juego y reglas del Tetris
- matriz.py: funciones de movimiento, consolidación y eliminación de filas
- idiomas.py: carga de textos según el idioma seleccionado
- idiomas/: archivos JSON con traducciones
- archivos_de_texto/: rankings y partidas guardadas
- imagenes/: recursos visuales del juego
- sonido/: efectos y música del juego

## Tecnologías utilizadas

- Python
- pygame
- tkinter
- archivos JSON y texto para configuraciones, idiomas y puntuaciones

## Nota final

Este proyecto fue pensado como una versión completa y personalizada de Tetris, ideal para practicar programación en Python, diseño de interfaces, lógica de juegos y manejo de recursos.

### Descripción para el repositorio

TetrisDEX es un proyecto en Python inspirado en el clásico Tetris, con múltiples modos de juego, personalización visual y sonora, sistema de puntuación, ranking y opciones para guardar y cargar partidas. Es una versión completa y entretenida para disfrutar jugando y practicar programación.
