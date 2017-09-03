import pyglet

window = pyglet.window.Window(width=400, height=400, config=pyglet.gl.Config(depth_size=24, double_buffer=True))

sound = pyglet.media.load('tada.wav', streaming=False)
play_sound = True

wall_positions = [(0, 0), (1, 0), (2, 0), (2, 1), (0, 2), (2, 2)]

player_position = (0, 1)
finish_position = (1, 3)

RUNNING_TIME = 0

# X roste doprava
# Y roste dolů
# Z roste k nám

def draw_cube():
    pyglet.graphics.draw_indexed(8,

                                 pyglet.gl.GL_TRIANGLE_STRIP,

                                 # Odkazy do n-tic níže
                                 [1, 0, 2, 3, 6, 7, 5, 4, 1, 0, 0, 4, 3, 7, 7, 6, 6, 5, 2, 1],

                                 # Vrcholy
                                 ('v3f', (-0.5, -0.5,  0.5,   # 0
                                          0.5,  -0.5,  0.5,   # 1
                                          0.5,   0.5,  0.5,   # 2
                                          -0.5,  0.5,  0.5,   # 3
                                          -0.5, -0.5, -0.5,   # 4
                                          0.5,  -0.5, -0.5,   # 5
                                          0.5,   0.5, -0.5,   # 6
                                          -0.5,  0.5, -0.5)), # 7

                                 # Barvy
                                 ('c3f', (0, 0, 1,   # 0
                                          1, 0, 1,   # 1
                                          1, 1, 1,   # 2
                                          0, 1, 1,   # 3
                                          0, 0, 0,   # 4
                                          1, 0, 0,   # 5
                                          1, 1, 0,   # 6
                                          0, 1, 0))) # 7


def draw_cube_at(x, y, scale=1, rotate=(0, 0, 0, 0)):
    pyglet.gl.glTranslatef(x, y, 0)
    pyglet.gl.glScalef(scale, scale, scale)
    pyglet.gl.glRotatef(*rotate)
    draw_cube()
    pyglet.gl.glRotatef(-rotate[0], *rotate[1:])
    pyglet.gl.glScalef(1 / scale, 1 / scale, 1 / scale)
    pyglet.gl.glTranslatef(-x, -y, 0)


@window.event
def on_key_press(symbol, modifier):
    global player_position

    x, y = player_position

    if symbol == pyglet.window.key.UP:
        new_player_position = x, y + 1
    elif symbol == pyglet.window.key.DOWN:
        new_player_position = x, y - 1
    elif symbol == pyglet.window.key.RIGHT:
        new_player_position = x + 1, y
    elif symbol == pyglet.window.key.LEFT:
        new_player_position = x - 1, y
    else:
        new_player_position = x, y

    if new_player_position not in wall_positions:
        player_position = new_player_position



@window.event
def on_show():
    # Režim GL_PROJECTION slouží k nastavování pohledu (dívání se) na svět: zorného pole, perspektivy atp. Jedná se
    # v podstatě o vlastnosti oka/kamery.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity() # Vyresetuje matici do výchozího stavu – zruší všechny transformace.

    fovy = 45.0 # Úhel, který vidíme.
    aspect = float(window.width) / window.height # Poměr stran
    zNear = 0.1 # Jak blízko vidíme. Hodně malé číslo.
    zFar = 320 # Jak daleko vidíme. Dost velké číslo na to, abychom viděli vše, co potřebujeme.
    pyglet.gl.gluPerspective(fovy, aspect, zNear, zFar)



@window.event
def on_draw():
    window.clear()

     # Režim GL_MODELVIEW slouží k nastavování pozice v e světě. Jedná se v podstatě o umístění postavy/kamery.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity() # Vyresetuje matici do výchozího stavu – zruší všechny transformace.

    # Normálně jsou všechny plochy vidět bez ohledu na to, zda se na to díváme zepředu, nebo zezadu. GL_CULL_FACE
    # zařídí, že jsou plochy vidět jen z jedné strany.
    pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
    pyglet.gl.glCullFace(pyglet.gl.GL_BACK) # Zadní stranu nevidíme.
    pyglet.gl.glFrontFace(pyglet.gl.GL_CW) # Přední strana je ta, která je nakreslená po směru hodinových ručiček.

    # Normálně vše nově vykreslené překryje to, co jsme vykreslili dříve. GL_DEPTH_TEST zařídí, že se při vykreslování
    # zohlední vzdálenost od porozovatele/kamery.
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
    pyglet.gl.glDepthFunc(pyglet.gl.GL_LEQUAL)

    # Posune pozorovatele/kameru trochu dozadu, ať něco vidíme: Kostku totiž kreslíme na nule. Není rozdíl mezi
    # posunutím všeho dopředu a pozorovatele/kamery dozaru.
    pyglet.gl.glTranslatef(0, 0, -6)

    pyglet.gl.glRotatef(0, 1, 1, 0)
    pyglet.gl.glScalef(0.5, 0.5, 0.5)

    # Walls.
    for wall_position in wall_positions:
        draw_cube_at(*wall_position)

    # Finish.
    draw_cube_at(*finish_position, 0.5, (90, 1, 1, 0))

    # Player.
    draw_cube_at(*player_position, 0.5)


def tick(dt):
    global RUNNING_TIME, play_sound
    RUNNING_TIME += dt

    if player_position == finish_position:
        if play_sound:
            sound.play()
        play_sound = False
    else:
        play_sound = True


pyglet.clock.schedule_interval(tick, 1 / 30)
pyglet.app.run()
