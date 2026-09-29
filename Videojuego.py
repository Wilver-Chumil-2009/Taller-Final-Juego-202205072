import pygame
import random

pygame.init()

# Pantalla
ANCHO = 600
ALTO = 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🏎️ Carrera de Carros")

# Colores
VERDE = (30, 140, 50)
GRIS = (70, 70, 70)
BLANCO = (255, 255, 255)
AZUL = (30, 100, 220)
ROJO = (220, 40, 40)
NEGRO = (20, 20, 20)
AMARILLO = (255, 220, 0)

reloj = pygame.time.Clock()

# Jugador
jugador = pygame.Rect(275, 570, 50, 90)
velocidad_jugador = 7

# Enemigos
enemigos = []
velocidad_enemigos = 6

# Puntuación
puntos = 0
fuente = pygame.font.Font(None, 40)

# Líneas de la carretera
lineas = []
for y in range(0, ALTO, 100):
    lineas.append(y)


def dibujar_carro(rectangulo, color):
    # Cuerpo
    pygame.draw.rect(
        pantalla,
        color,
        rectangulo,
        border_radius=8
    )

    # Ventanas
    pygame.draw.rect(
        pantalla,
        (150, 210, 240),
        (rectangulo.x + 8, rectangulo.y + 10, 34, 25),
        border_radius=5
    )

    pygame.draw.rect(
        pantalla,
        (150, 210, 240),
        (rectangulo.x + 8, rectangulo.y + 50, 34, 20),
        border_radius=5
    )

    # Luces
    pygame.draw.rect(
        pantalla,
        AMARILLO,
        (rectangulo.x + 5, rectangulo.y + 2, 10, 7)
    )

    pygame.draw.rect(
        pantalla,
        AMARILLO,
        (rectangulo.x + 35, rectangulo.y + 2, 10, 7)
    )


def dibujar_carretera():
    pantalla.fill(VERDE)

    # Carretera
    pygame.draw.rect(
        pantalla,
        GRIS,
        (150, 0, 300, ALTO)
    )

    # Bordes
    pygame.draw.rect(
        pantalla,
        BLANCO,
        (145, 0, 5, ALTO)
    )

    pygame.draw.rect(
        pantalla,
        BLANCO,
        (450, 0, 5, ALTO)
    )

    # Líneas centrales
    for y in lineas:
        pygame.draw.rect(
            pantalla,
            BLANCO,
            (295, y, 10, 60)
        )


def crear_enemigo():
    x = random.choice([175, 225, 275, 325, 375])
    enemigo = pygame.Rect(x, -100, 50, 90)
    enemigos.append(enemigo)


def pantalla_game_over():
    pantalla.fill(NEGRO)

    texto = fuente.render(
        "GAME OVER",
        True,
        ROJO
    )

    pantalla.blit(
        texto,
        (ANCHO // 2 - texto.get_width() // 2, 280)
    )

    texto_puntos = fuente.render(
        f"Puntos: {puntos}",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_puntos,
        (ANCHO // 2 - texto_puntos.get_width() // 2, 340)
    )

    texto_reinicio = fuente.render(
        "Presiona ENTER para reiniciar",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_reinicio,
        (ANCHO // 2 - texto_reinicio.get_width() // 2, 400)
    )

    pygame.display.update()


# Juego
ejecutando = True
game_over = False
contador = 0

while ejecutando:

    reloj.tick(60)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if game_over and evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_RETURN:
                jugador.x = 275
                jugador.y = 570
                enemigos.clear()
                puntos = 0
                velocidad_enemigos = 6
                game_over = False

    if not game_over:

        # Controles
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            jugador.x -= velocidad_jugador

        if teclas[pygame.K_RIGHT]:
            jugador.x += velocidad_jugador

        if teclas[pygame.K_UP]:
            jugador.y -= velocidad_jugador

        if teclas[pygame.K_DOWN]:
            jugador.y += velocidad_jugador

        # Limitar jugador
        if jugador.left < 155:
            jugador.left = 155

        if jugador.right > 445:
            jugador.right = 445

        if jugador.top < 0:
            jugador.top = 0

        if jugador.bottom > ALTO:
            jugador.bottom = ALTO

        # Movimiento de carretera
        for i in range(len(lineas)):
            lineas[i] += velocidad_enemigos

            if lineas[i] > ALTO:
                lineas[i] = -60

        # Crear enemigos
        contador += 1

        if contador >= 50:
            crear_enemigo()
            contador = 0

        # Mover enemigos
        for enemigo in enemigos:
            enemigo.y += velocidad_enemigos

        # Eliminar enemigos
        enemigos = [
            enemigo
            for enemigo in enemigos
            if enemigo.y < ALTO
        ]

        # Detectar choques
        for enemigo in enemigos:
            if jugador.colliderect(enemigo):
                game_over = True

        # Puntos
        puntos += 1

        # Aumentar dificultad
        if puntos % 1000 == 0:
            velocidad_enemigos += 1

        # Dibujar
        dibujar_carretera()

        dibujar_carro(
            jugador,
            AZUL
        )

        for enemigo in enemigos:
            dibujar_carro(
                enemigo,
                ROJO
            )

        # Mostrar puntos
        texto = fuente.render(
            f"Puntos: {puntos // 10}",
            True,
            BLANCO
        )

        pantalla.blit(
            texto,
            (20, 20)
        )

        pygame.display.update()

    else:
        pantalla_game_over()


pygame.quit()
