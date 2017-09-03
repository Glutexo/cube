import pyglet, time

window = pyglet.window.Window()

obrazek = pyglet.image.load('had.png')
had = pyglet.sprite.Sprite(obrazek)

i = 0

@window.event
def on_draw():
    window.clear()
    pyglet.gl.glPushMatrix()

    pyglet.gl.glTranslatef(had.width / 2, had.height / 2, 0)
    pyglet.gl.glRotatef(i * 10, 0, 1, 0)
    pyglet.gl.glTranslatef(-had.width / 2, -had.height / 2, 0)

    had.draw()

    pyglet.gl.glPopMatrix()


def tick(dt):
    global i
    i += dt
    pass

pyglet.clock.schedule_interval(tick, 1/4)
pyglet.app.run()
