from random import choice
from turtle import *
from freegames import floor, vector

# Estado del juego, que almacena la puntuación
state = {'score': 0}

# Turtles para dibujar el mundo y escribir la puntuación
path = Turtle(visible=False)
writer = Turtle(visible=False)

# Dirección inicial de Pacman
aim = vector(5, 0)

# Posición inicial de Pacman
pacman = vector(-40, -80)

# Lista de fantasmas con su posición inicial y dirección de movimiento
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# Mapa del juego (1 representa caminos con puntos, 0 representa paredes)
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y):
    """Dibuja un cuadrado usando el Turtle path en la posición (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    """Devuelve el índice del punto en la lista de tiles, es decir, nos dice si 
    el pacman esta en un camino o en la pared"""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    """Devuelve True si el punto es válido dentro del mapa."""
    index = offset(point)

    # Verifica si el punto es una pared
    if tiles[index] == 0:
        return False

    index = offset(point + 19)
    
    # Verifica nuevamente para evitar que se sobrepase una pared
    if tiles[index] == 0:
        return False

    # Permite el movimiento si está alineado con la cuadrícula
    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Dibuja el mundo del juego usando el Turtle path."""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            
            # Dibuja puntos blancos donde haya comida
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Mueve a Pacman y a los fantasmas."""
    writer.undo()
    writer.write(state['score'])

    clear()
    
    # Verifica si el movimiento de Pacman es válido
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    # Si Pacman encuentra comida, la elimina y aumenta la puntuación
    if tiles[index] == 1:
        tiles[index] = 2 # Marca la comida como comida
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    # Dibuja a Pacman
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    # Mueve a los fantasmas
    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            # Si el fantasma choca con una pared, cambia de dirección aleatoriamente
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            
            # Filtrar direcciones válidas (evitar paredes)
            valid_moves = [move for move in options if valid(point + move)]

            if valid_moves:
                # Elegir la dirección más cercana a Pac-Man
                best_move = min(valid_moves, key=lambda move: abs((point + move) - pacman))
                course.x = best_move.x
                course.y = best_move.y
            else:
                # Si no hay movimientos válidos, mantener uno aleatorio
                course.x, course.y = choice(options).x, choice(options).y
            

        # Dibuja a los fantasmas
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    # Verifica si Pacman ha sido atrapado por un fantasma
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return # Termina el juego si un fantasma toca a Pacman

    ontimer(move, 100)  # Llama a la función `move` cada 100ms

def change(x, y):
    """Cambia la dirección de Pacman si el movimiento es válido."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

# Configuración de la ventana del juego
setup(420, 420, 370, 0)
hideturtle()
tracer(False)

# Configuración del marcador de puntuación
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()

# Configuración de controles para Pacman
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

# Inicia el juego
world()
move()
done()
