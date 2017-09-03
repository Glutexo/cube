import itertools

import pyglet

def _to_index(string):
    if not string:
        return 0
    else:
        return int(string)


def load_obj_to_batch(file, batch, group=None):
    vertices = [(0, 0, 0)]
    texture_coords = [(0, 0)]
    vertex_normals = [(0, 0, 0)]

    vertices_for_index = {}
    vertex_data = []
    indices = []

    for line in file:
        line = line.strip()
        if line.startswith('#'):
            continue
        parts = line.strip().split()
        line_type = parts[0]
        args = parts[1:]

        if line_type in ('mtllib', 'usemtl', 's', 'o'):
            print('Unsupported feature: ' + line_type)
        elif line_type == 'v':
            vertices.append(tuple(float(c) for c in args[:3]))
        elif line_type == 'vt':
            texture_coords.append(tuple(float(c) for c in args[:2]))
        elif line_type == 'vn':
            vertex_normals.append(tuple(float(c) for c in args[:3]))
        elif line_type == 'f':
            if len(args) == 3:
                tri_indices = 0, 1, 2
            if len(args) == 4:
                tri_indices = 0, 1, 2, 2, 1, 3
            for i in tri_indices:
                items = [_to_index(n) for n in args[i].split('/')]
                data = (
                    *vertices[items[0]],
                    *texture_coords[items[1]],
                    *vertex_normals[items[2]],
                )
                index = vertices_for_index.get(data)
                if index is None:
                    index = len(vertex_data)
                    vertices_for_index[data] = index
                    vertex_data.append(data)
                indices.append(index)
        else:
            raise ValueError('Unsupported feature: ' + line_type)

    _fi = itertools.chain.from_iterable
    batch.add_indexed(
        len(vertex_data),
        pyglet.gl.GL_TRIANGLES,
        group,
        indices,
        ('v3f', list(_fi((x, y, z) for x, y, z, u, v, nx, ny, nz in vertex_data))),
        ('t2f', list(_fi((u, v) for x, y, z, u, v, nx, ny, nz in vertex_data))),
        ('n3f', list(_fi((nx, ny, nz) for x, y, z, u, v, nx, ny, nz in vertex_data))),
    )
