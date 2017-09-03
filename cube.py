import pyglet

window = pyglet.window.Window(width=400, height=400, config=pyglet.gl.Config(depth_size=24, double_buffer=True))
companion_cube = pyglet.image.load('companion_cube.png')
texture_region = companion_cube.get_texture()

position = [0, 1, 0]

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

    window.clear()

    pyglet.gl.glColor3f(1, 1, 1)

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
    global i
    i += dt

pyglet.clock.schedule_interval(tick, 1/30)
pyglet.app.run()
