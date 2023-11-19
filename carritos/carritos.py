# Importamos la biblioteca pygame y algunos módulos específicos.
import pygame
from pygame.locals import *
import random
# Inicializamos pygame.
pygame.init()
pygame.mixer.init()

# Creamos la ventana del juego con las dimensiones especificadas.
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Coche del Profe') # Título de la ventana del juego.

# Definimos algunos colores que usaremos en el juego.
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Definimos el ancho de la carretera y las marcas del carril.
road_width = 300
marker_width = 10
marker_height = 50

# Coordenadas de los carriles.
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Marcadores y bordes de la carretera.
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# for animating movement of the lane markers
lane_marker_move_y = 0

# Coordenadas iniciales del jugador.
player_x = 250
player_y = 400

# Configuraciones de los frames.
clock = pygame.time.Clock()
fps = 120

# Configuraciones del juego.
gameover = False
speed = 2
score = 0

# Inicializamos el mezclador de sonido de pygame (agregar esto después de pygame.init())
pygame.mixer.init()

# Cargar el archivo de sonido
car_sound = pygame.mixer.Sound('audio/audio.wav')
car_sound.set_volume(0.5)  # Ajustar el volumen a un 50%
# Cargar el sonido de colisión
collision_sound = pygame.mixer.Sound('audio/crash.wav')  # Asegúrate de que el archivo 'collision.wav' esté en la carpeta 'sounds'


# Reproducir el sonido del coche continuamente en el fondo
car_sound.play(-1)  # El argumento -1 hace que el sonido se repita indefinidamente


# Clase para los vehículos.
class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Escalamos la imagen para que no sea más ancha que el carril.
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

# Clase para el vehículo del jugador.
class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)

# Grupos de sprites para el jugador y otros vehículos.
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Creamos el coche del jugador.
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Cargamos las imágenes de los vehículos.
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)

# Cargamos la imagen del choque.
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

# Bucle principal del juego.
running = True
while running:

    clock.tick(fps)
    # Eventos de pygame, como cerrar la ventana o presionar teclas.
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False


        # Mover el coche del jugador con las teclas de flecha.

        if event.type == KEYDOWN:
            # Resto de código para manejar el movimiento y las colisiones...
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

            # comprobar si hay una colisión lateral después de cambiar de carril
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):

                    gameover = True

                    # coloca el auto del jugador al lado de otro vehículo
                    # determine dónde colocar la imagen del accidente
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]


    # dibujar la hierba
    screen.fill(green)

    # dibujar el camino
    pygame.draw.rect(screen, gray, road)

    # dibujar los marcadores de borde
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # dibujar los marcadores de carril
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    # dibuja el auto del jugador
    player_group.draw(screen)

    # agregar un vehículo
    if len(vehicle_group) < 2:

        # asegúrese de que haya suficiente espacio entre los vehículos
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:

            # selecciona un carril aleatorio
            lane = random.choice(lanes)

            # seleccione una imagen de vehículo aleatoria
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)

    # hacer que los vehículos se muevan
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        # eliminar el vehículo una vez que sale de la pantalla
        if vehicle.rect.top >= height:
            vehicle.kill()

            # agregar a la puntuación
            score += 1

            # acelera el juego después de pasar 5 vehículos
            if score > 0 and score % 5 == 0:
                speed += 1

    # dibujar los vehículos
    vehicle_group.draw(screen)

    # mostrar la puntuación
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    screen.blit(text, text_rect)

    # comprobar si hay una colisión frontal
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
        # Detener la reproducción del sonido del motor cuando chocas.
        collision_sound.play()

        car_sound.stop()
    # mostrar juego terminado
    if gameover:
        screen.blit(crash, crash_rect)

        pygame.draw.rect(screen, red, (0, 50, width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)

    pygame.display.update()

    # esperar  si acepta usuario para volver a jugar o salir
    while gameover:

        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == QUIT:
                gameover = False
                running = False

            # obtener la entrada del usuario (y o n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # restablecer el juego
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # salir de los bucles
                    gameover = False
                    running = False

pygame.quit()