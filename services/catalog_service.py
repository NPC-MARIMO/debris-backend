from collections import defaultdict

# Object Catalog Storage
catalog = defaultdict(list)

def add_observation(object_id, pixel_x, pixel_y, timestamp):

    catalog[object_id].append({
        "pixel_x": pixel_x,
        "pixel_y": pixel_y,
        "timestamp": timestamp
    })

    return True


def get_object_history(object_id):

    return catalog.get(object_id, [])
    