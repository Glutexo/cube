import pyglet

cubeWindow = pyglet.window.Window(width=400, height=400, config=pyglet.gl.Config(depth_size=24, double_buffer=True))
companion_cube = pyglet.image.load('companion_cube.png')
texture_region = companion_cube.get_texture()

i = 0

@cubeWindow.event
def on_show():
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
    # Set up projection matrix.
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()
    pyglet.gl.gluPerspective(45.0, float(cubeWindow.width) / cubeWindow.height, 0.1, 360)


@cubeWindow.event
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
    pyglet.gl.glRotatef(i * 50, 1, 1, 0)  # seems to rotate c degrees around a point x,y,z???

    cubeWindow.clear()

    pyglet.gl.glColor4f(1.0, 0, 0, 1.0)

    pyglet.graphics.draw_indexed(8, pyglet.gl.GL_LINES, [0, 1, 1, 2, 2, 3, 3, 0,  # front square
                                                         4, 5, 5, 6, 6, 7, 7, 4,  # back square
                                                         0, 4, 1, 5, 2, 6, 3, 7],  # connectors
                                 ('v3f', (-1, -1, 1,
                                          1, -1, 1,
                                          1, 1, 1,
                                          -1, 1, 1,
                                          -1, -1, -1,
                                          1, -1, -1,
                                          1, 1, -1,
                                          -1, 1, -1)),
                                 ('c3f', (0, 0, 1,
                                          1, 0, 1,
                                          1, 1, 1,
                                          0, 1, 1,
                                          0, 0, 0,
                                          1, 0, 0,
                                          1, 1, 0,
                                          0, 1, 0)))

    pyglet.gl.glScalef(0.5, 0.5, 0.5)

    pyglet.graphics.draw_indexed(8, pyglet.gl.GL_TRIANGLE_STRIP, [1, 0, 2, 3, 6, 7, 5, 4, 1, 0, 0, 4, 3, 7, 7, 6, 6, 5, 2, 1],
                                 ('v3f', (-1, -1, 1, # 0
                                          1, -1, 1, # 1
                                          1, 1, 1, # 2
                                          -1, 1, 1, # 3
                                          -1, -1, -1, # 4
                                          1, -1, -1, # 5
                                          1, 1, -1, # 6
                                          -1, 1, -1)), # 7
                                 ('c3f', (0, 0, 1,
                                          1, 0, 1,
                                          1, 1, 1,
                                          0, 1, 1,
                                          0, 0, 0,
                                          1, 0, 0,
                                          1, 1, 0,
                                          0, 1, 0)))

    pyglet.gl.glScalef(1.5, 1.5, 1.5)

    pyglet.gl.glColor3f(1, 1, 1)

    pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)
    pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, texture_region.id)

    # actual_width = companion_cube.width / texture_region.texture.width
    actual_width = companion_cube.width / 512

    pyglet.graphics.draw_indexed(8, pyglet.gl.GL_TRIANGLE_STRIP, [1, 0, 2, 3, 6, 7, 5, 4, 1, 0, 0, 4, 3, 7, 7, 6, 6, 5, 2, 1],
                                 ('v3f', (-1, -1, 1, # 0
                                          1, -1, 1, # 1
                                          1, 1, 1, # 2
                                          -1, 1, 1, # 3
                                          -1, -1, -1, # 4
                                          1, -1, -1, # 5
                                          1, 1, -1, # 6
                                          -1, 1, -1)), # 7
                                 ('t2f', (0, 0,
                                          actual_width, 0,
                                          actual_width, actual_width,
                                          0, actual_width,
                                          0, 0,
                                          actual_width, 0,
                                          actual_width, actual_width,
                                          0, actual_width)))

    pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, 0)
    pyglet.gl.glDisable(pyglet.gl.GL_TEXTURE_2D)


def tick(dt):
    global i
    i += dt

pyglet.clock.schedule_interval(tick, 1/30)
pyglet.app.run()
