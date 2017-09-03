import pyglet

window = pyglet.window.Window(width=400, height=400, config=pyglet.gl.Config(depth_size=24, double_buffer=True))

sound = pyglet.media.load('tada.wav', streaming=False)
play_sound = True

max_y = 0
with open('maze.txt', 'r') as file:
    data = {}
    for y, line in enumerate(file):
        line = line.strip('\n')
        for x, char in enumerate(line):
            data[x, y] = char
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
    elif char == 'F':
        finish_position = translated_position

i = 0


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
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
    # Set up projection matrix.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluPerspective(45.0, float(window.width) / window.height, 0.1, 360)


@window.event
def on_draw():
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
    pyglet.gl.glDepthFunc(pyglet.gl.GL_LEQUAL)

    pyglet.gl.glEnable(pyglet.gl.GL_CULL_FACE)
    pyglet.gl.glFrontFace(pyglet.gl.GL_CW)
    pyglet.gl.glCullFace(pyglet.gl.GL_BACK)

    # Move the camera back a little.
    # TODO(sam): When you want to start rotating the camera, this should move into on_draw,
    # and there should be a call to gRotatef.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.glTranslatef(0, 0, -6)
    # pyglet.gl.glRotatef(i * 50, 1, 1, 0)  # seems to rotate c degrees around a point x,y,z???
    pyglet.gl.glRotatef(0, 1, 1, 0)  # seems to rotate c degrees around a point x,y,z???
    pyglet.gl.glScalef(0.5, 0.5, 0.5)

    pyglet.gl.glTranslatef(-player_position[0], -player_position[1], 0)

    window.clear()

    pyglet.gl.glColor3f(1, 1, 1)

    # Walls.
    for wall_position in wall_positions:
        draw_cube_at(*wall_position)

    # Finish.
    draw_cube_at(*finish_position, 0.5, (90, 1, 1, 0))

    # Player.
    draw_cube_at(*player_position, 0.5)


def tick(dt):
    global i, play_sound
    i += dt

    if player_position == finish_position:
        if play_sound:
            sound.play()
        play_sound = False
    else:
        play_sound = True


pyglet.clock.schedule_interval(tick, 1/30)
pyglet.app.run()
