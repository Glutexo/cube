import pyglet

window = pyglet.window.Window(width=400, height=400, config=pyglet.gl.Config(depth_size=24, double_buffer=True))

position = [0, 1, 0]

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

@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.UP:
        position[1] += 1
    elif symbol == pyglet.window.key.DOWN:
        position[1] -= 1
    elif symbol == pyglet.window.key.RIGHT:
        position[0] += 1
    elif symbol == pyglet.window.key.LEFT:
        position[0] -= 1


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

    draw_cube()
    pyglet.gl.glTranslatef(1, 0, 0)
    draw_cube()
    pyglet.gl.glTranslatef(1, 0, 0)
    draw_cube()
    pyglet.gl.glTranslatef(0, 1, 0)
    draw_cube()
    pyglet.gl.glTranslatef(-2, 1, 0)
    draw_cube()
    pyglet.gl.glTranslatef(2, 0, 0)
    draw_cube()

    pyglet.gl.glTranslatef(-2, -2, 0)
    pyglet.gl.glTranslatef(*position)
    pyglet.gl.glScalef(0.5, 0.5, 0.5)
    draw_cube()


def tick(dt):
    global RUNNING_TIME
    RUNNING_TIME += dt


pyglet.clock.schedule_interval(tick, 1 / 30)
pyglet.app.run()
