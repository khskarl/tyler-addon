def all_tile_ids():
    return [id for id in range(1, 2**8)]


def unique_tile_ids():
    ids = all_tile_ids()

    for i in range(0, len(ids)):
        # Check if we still have a valid 'i' after 'del ids[j]'
        if i >= len(ids):
            break

        uid = ids[i]
        print(uid)
        rotations = get_rotations_ids(uid)

        if uid == 16:
            print(rotations)
        for j in range(i + 1, len(ids)):
            for rotation in rotations:
                # Check if we still have a valid 'j' after 'del ids[j]'
                if j >= len(ids):
                    break
                if ids[j] == rotation:
                    del ids[j]
    return ids


def get_rotations_ids(r0):
    r1 = rotate_tile(r0)
    r2 = rotate_tile(r1)
    r3 = rotate_tile(r2)

    return [r1, r2, r3]


def rotate_tile(tile_id):
    upper_layer = (tile_id & 0xF0) >> 4
    lower_layer = tile_id & 0x0F

    upper_layer = rotate_layer(upper_layer) << 4
    lower_layer = rotate_layer(lower_layer)

    return upper_layer | lower_layer


def rotate_layer(layer_mask):
    c0 = layer_mask & 0b0001
    c1 = layer_mask & 0b0010
    c2 = layer_mask & 0b0100
    c3 = layer_mask & 0b1000

    c0 = rotate_cell(c0)
    c1 = rotate_cell(c1)
    c2 = rotate_cell(c2)
    c3 = rotate_cell(c3)

    return c3 | c2 | c1 | c0


def rotate_cell(cell_mask):
    map = {
        0b0001: 0b0010,
        0b0010: 0b1000,
        0b1000: 0b0100,
        0b0100: 0b0001,
        0b0000: 0b0000,
    }

    return map[cell_mask]


if __name__ == "__main__":
    unique = unique_tile_ids()
    print(len(unique))
    print(unique)
