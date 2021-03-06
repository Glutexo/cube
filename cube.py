import pyglet, batch_loader, contextlib

window = pyglet.window.Window(width=800, height=800, config=pyglet.gl.Config(depth_size=24, double_buffer=True))
pressed_keys = set()

sound = pyglet.media.load('tada.wav', streaming=False)
play_sound = True

camera_mode = 1 # Supported modes: 1, 3

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


def vec(*args):
    return (pyglet.gl.GLfloat * len(args))(*args)


def draw_cube():
    pyglet.graphics.draw_indexed(8, pyglet.gl.GL_TRIANGLE_STRIP, [1, 0, 2, 3, 6, 7, 5, 4, 1, 0, 0, 4, 3, 7, 7, 6, 6, 5, 2, 1],
                                 ('v3f', (-0.5, -0.5, 0.5, # 0
                                          0.5, -0.5, 0.5, # 0.5
                                          0.5, 0.5, 0.5, # 2
                                          -0.5, 0.5, 0.5, # 3
                                          -0.5, -0.5, -0.5, # 4
                                          0.5, -0.5, -0.5, # 5
                                          0.5, 0.5, -0.5, # 6
                                          -0.5, 0.5, -0.5)), # 7
                                 ('c3f', (0, 0, 1,
                                          1, 0, 1,
                                          1, 1, 1,
                                          0, 1, 1,
                                          0, 0, 0,
                                          1, 0, 0,
                                          1, 1, 0,
                                          0, 1, 0)))

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
    pressed_keys.discard(symbol)


@window.event
def on_key_press(symbol, modifier):
    global camera_mode
    if symbol == pyglet.window.key.SPACE:
        if camera_mode == 1:
            camera_mode = 3
        else:
            camera_mode = 1
    else:
        pressed_keys.add(symbol)


@window.event
def on_show():
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
    # Set up projection matrix.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    # pyglet.gl.gluPerspective(45.0, float(window.width) / window.height, 0.1, 360)
    pyglet.gl.gluPerspective(60.0, float(window.width) / window.height, 0.1, 360)


@window.event
def on_draw():
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
    pyglet.gl.glDepthFunc(pyglet.gl.GL_LEQUAL)

    pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
    pyglet.gl.glCullFace(pyglet.gl.GL_BACK)

    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()

    if camera_mode == 1:
        pyglet.gl.glRotatef(90, 0, 1, 0)
        pyglet.gl.glRotatef(-90, 1, 0, 0)
        pyglet.gl.glTranslatef(0.3, 0, 0)
        pyglet.gl.glRotatef(-player_rotation + 90, 0, 0, 1)
    elif camera_mode == 3:
        pyglet.gl.glTranslatef(0, 0, -6)
        pyglet.gl.glRotatef(-15, 1, 1, 0)
        # pyglet.gl.glRotatef(i * 50, 1, 1, 0)

    pyglet.gl.glScalef(0.5, 0.5, 0.5)

    pyglet.gl.glTranslatef(-player_position[0], -player_position[1], 0)

    pyglet.gl.glClearColor(0.7, 0.7, 0.7, 1)
    window.clear()

    pyglet.gl.glColor3f(1, 1, 1)

    # Walls.
    for wall_position in wall_positions:
        draw_cube_at(*wall_position)

    pyglet.gl.glEnable(pyglet.gl.GL_LIGHTING)
    pyglet.gl.glEnable(pyglet.gl.GL_COLOR_MATERIAL)
    pyglet.gl.glEnable(pyglet.gl.GL_LIGHT0)
    pyglet.gl.glLightfv(pyglet.gl.GL_LIGHT0, pyglet.gl.GL_POSITION, vec(10, 10, 10))
    pyglet.gl.glLightfv(pyglet.gl.GL_LIGHT0, pyglet.gl.GL_DIFFUSE, vec(1, 1, 1, 1))
    pyglet.gl.glMaterialfv(pyglet.gl.GL_FRONT, pyglet.gl.GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0.5, 0.5, 1))

    # Finish.
    draw_batch_at(finish_batch, finish_texture_region, *finish_position, 0.005, ((90, 1, 0, 0),))

    # Player.
    if camera_mode == 3:
        draw_batch_at(player_batch, player_texture_region, *player_position, 0.25, ((player_rotation, 0, 0, 1), (90, 1, 0, 0)))


def tick(dt):
    global i, play_sound, player_position, player_rotation, source_player_position, target_player_position, source_player_rotation, target_player_rotation, player_animation_dt
    i += dt

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


pyglet.clock.schedule_interval(tick, 1/30)
pyglet.app.run()
