import pyglet, batch_loader, contextlib

window = pyglet.window.Window(width=800, height=800, config=pyglet.gl.Config(depth_size=24, double_buffer=True))
pressed_keys = set()

sound = pyglet.media.load('tada.wav', streaming=False)
play_sound = True

# Model from: https://opengameart.org/content/treasure-chest-3
# (but use a cleaned-up model instead of the one from there)!
finish_image = pyglet.image.load('Treasurechest_DIFF.png')
finish_texture_region = finish_image.get_texture()

player_image = pyglet.image.load('texture.png')
player_texture_region = player_image.get_texture()

finish_batch = pyglet.graphics.Batch()
player_batch = pyglet.graphics.Batch()

with open('chest.obj') as chest_obj:
    batch_loader.load_obj_to_batch(chest_obj, finish_batch)

with open('slimemodel.obj') as slimemodel_obj:
    batch_loader.load_obj_to_batch(slimemodel_obj, player_batch)

max_y = 0
with open('maze.txt', 'r') as file:
    data = {}
    for y, line in enumerate(file):
        line = line.strip('\n')
        for x, char in enumerate(line):
            data[x, y] = char

            # Flip the map vertically, as Y raises upwards.
            if y > max_y:
                max_y = y

wall_positions = []
for file_position, char in data.items():
    translated_position = (file_position[0], max_y - file_position[1])
    # translated_position = (file_position[0], file_position[1])
    if char == 'W':
        wall_positions.append(translated_position)
    elif char == 'S':
        player_position = translated_position
        source_player_position, target_player_position = player_position, player_position
    elif char == 'F':
        finish_position = translated_position

i = 0
player_rotation = 90
source_player_rotation = target_player_rotation = player_rotation
player_animation_dt = 0
player_animation_duration = 0.3

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

@contextlib.contextmanager
def pushed_matrix_at(x, y, scale=1, rotate=()):
    pyglet.gl.glPushMatrix()
    pyglet.gl.glTranslatef(x, y, 0)
    pyglet.gl.glScalef(scale, scale, scale)
    for r in rotate:
        pyglet.gl.glRotatef(*r)
    yield
    pyglet.gl.glPopMatrix()


def draw_cube_at(x, y, scale=1, rotate=()):
    pyglet.gl.glFrontFace(pyglet.gl.GL_CW)
    with pushed_matrix_at(x, y, scale, rotate):
        draw_cube()


def draw_batch_at(batch, texture, x, y, scale=1, rotate=()):
    pyglet.gl.glFrontFace(pyglet.gl.GL_CCW)
    with pushed_matrix_at(x, y, scale, rotate):
        pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, texture.id)

        batch.draw()

        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, 0)
        pyglet.gl.glDisable(pyglet.gl.GL_TEXTURE_2D)

@window.event
def on_key_release(symbol, modifier):
    pressed_keys.remove(symbol)


@window.event
def on_key_press(symbol, modifier):
    pressed_keys.add(symbol)


@window.event
def on_show():
    # Režim GL_PROJECTION slouží k nastavování pohledu (dívání se) na svět: zorného pole, perspektivy atp. Jedná se
    # v podstatě o vlastnosti oka/kamery.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity() # Vyresetuje matici do výchozího stavu – zruší všechny transformace.

    # fovy = 45.0 # Úhel, který vidíme.
    fovy = 60.0 # Úhel, který vidíme.
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

    pyglet.gl.glRotatef(90, 0, 1, 0)
    pyglet.gl.glRotatef(-90, 1, 0, 0)
    pyglet.gl.glTranslatef(0.3, 0, 0)
    pyglet.gl.glRotatef(-player_rotation + 90, 0, 0, 1)

    pyglet.gl.glScalef(0.5, 0.5, 0.5)

    pyglet.gl.glTranslatef(-player_position[0], -player_position[1], 0)

    pyglet.gl.glClearColor(0.7, 0.7, 0.7, 1)

    # Walls.
    for wall_position in wall_positions:
        draw_cube_at(*wall_position)

    # Finish.
    draw_batch_at(finish_batch, finish_texture_region, *finish_position, 0.005, ((90, 1, 0, 0),))

    # Player.
    # draw_batch_at(player_batch, player_texture_region, *player_position, 0.25, ((player_rotation, 0, 0, 1), (90, 1, 0, 0)))


def tick(dt):
    global RUNNING_TIME, play_sound, player_position, player_rotation, source_player_position, target_player_position, source_player_rotation, target_player_rotation, player_animation_dt
    RUNNING_TIME += dt

    if player_position == finish_position:
        if play_sound:
            sound.play()
        play_sound = False
    else:
        play_sound = True

    if player_position == target_player_position and player_rotation == target_player_rotation % 360:
        player_animation_dt = 0
        source_player_position = player_position
        source_player_rotation = target_player_rotation = player_rotation
        updated_player_position_x,  updated_player_position_y = player_position

        if pyglet.window.key.UP in pressed_keys:
            if player_rotation == 0:
                updated_player_position_y -= 1
            elif player_rotation == 90:
                updated_player_position_x += 1
            elif player_rotation == 180:
                updated_player_position_y += 1
            elif player_rotation == 270:
                updated_player_position_x -= 1
        if pyglet.window.key.DOWN in pressed_keys:
            if player_rotation == 0:
                updated_player_position_y += 1
            elif player_rotation == 90:
                updated_player_position_x -= 1
            elif player_rotation == 180:
                updated_player_position_y -= 1
            elif player_rotation == 270:
                updated_player_position_x += 1
        if pyglet.window.key.RIGHT in pressed_keys:
            target_player_rotation -= 90
        if pyglet.window.key.LEFT in pressed_keys:
            target_player_rotation += 90

        updated_player_position = updated_player_position_x, updated_player_position_y

        if updated_player_position not in wall_positions:
            target_player_position = updated_player_position
    else:
        player_animation_dt += dt
        player_position_delta = (
            target_player_position[0] - source_player_position[0],
            target_player_position[1] - source_player_position[1]
        )
        player_rotation_delta = target_player_rotation - source_player_rotation

        player_animation_coef = player_animation_dt / player_animation_duration
        if player_animation_coef >= 1:
            player_animation_coef = 1
        player_position = (
            source_player_position[0] + player_position_delta[0] * player_animation_coef,
            source_player_position[1] + player_position_delta[1] * player_animation_coef
        )
        player_rotation = (source_player_rotation + player_rotation_delta * player_animation_coef) % 360


pyglet.clock.schedule_interval(tick, 1 / 30)
pyglet.app.run()
