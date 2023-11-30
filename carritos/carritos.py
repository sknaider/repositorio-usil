import pygame
import random

# Inicialización de Pygame y configuración básica
pygame.init()
pygame.mixer.init()

# Configuraciones de la ventana del juego
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Coche del Profe')

# Colores y dimensiones
colors = {
    'gray': (100, 100, 100),
    'blue': (76, 208, 56),
    'red': (200, 0, 0),
    'white': (255, 255, 255),
    'yellow': (255, 232, 0)
}
road_width, marker_width, marker_height = 300, 10, 50
lanes = [150, 250, 350]  # Coordenadas de los carriles

# Configuraciones del jugador y el juego
player_pos = [250, 400]
fps, speed, score = 120, 2, 0
gameover = False

# Carga de sonidos
car_sound = pygame.mixer.Sound('audio/audio.wav')
car_sound.set_volume(0.5)
collision_sound = pygame.mixer.Sound('audio/crash.wav')
car_sound.play(-1)

# Clase Vehículo
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))

# Carga de imágenes
vehicle_images = ['images/' + name for name in ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']]
crash_image = pygame.image.load('images/crash.png')

# Grupos de Sprites
player = Vehicle('images/car.png', *player_pos)
all_vehicles = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle(player)

# Función para agregar vehículos
def add_vehicle():
    if len(all_vehicles) < 2 and not any(v.rect.top < v.rect.height * 1.5 for v in all_vehicles):
        lane = random.choice(lanes)
        image_path = random.choice(vehicle_images)
        all_vehicles.add(Vehicle(image_path, lane, -50))

# Bucle principal del juego
running = True
while running:
    screen.fill(colors['blue'])  # Fondo
    pygame.draw.rect(screen, colors['gray'], (100, 0, road_width, height))  # Carretera

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Manejo de eventos del teclado aquí...
        # Manejo de eventos del teclado para mover el coche
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.rect.centerx > lanes[0]:
                player.rect.centerx -= 100  # Mover a la izquierda
            if event.key == pygame.K_RIGHT and player.rect.centerx < lanes[-1]:
                player.rect.centerx += 100  # Mover a la derecha
    # Actualización y dibujo de sprites
    player_group.draw(screen)
    all_vehicles.draw(screen)
    add_vehicle()  # Agregar vehículos

    for vehicle in all_vehicles:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1

    # Detección de colisiones y manejo del juego terminado
    if pygame.sprite.spritecollide(player, all_vehicles, True):

        gameover = True
        # Manejo del juego terminado aquí...

    pygame.display.update()
    pygame.time.Clock().tick(fps)

pygame.quit()
