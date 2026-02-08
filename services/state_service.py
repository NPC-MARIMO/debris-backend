import numpy as np
from services.catalog_service import catalog

def pixel_to_space(pixel_x, pixel_y):
    """
    Temporary simulation mapping.
    Replace later with real astrometry.
    """

    scale = 0.1  # km per pixel (example)

    x = pixel_x * scale
    y = pixel_y * scale
    z = 0

    return np.array([x, y, z])


def compute_state_vector(object_id):

    obs = catalog.get(object_id)

    if not obs or len(obs) < 2:
        return None

    o1 = obs[-2]
    o2 = obs[-1]

    p1 = pixel_to_space(o1["pixel_x"], o1["pixel_y"])
    p2 = pixel_to_space(o2["pixel_x"], o2["pixel_y"])

    t1 = o1["timestamp"]
    t2 = o2["timestamp"]

    dt = t2 - t1

    if dt <= 0:
        return None

    velocity = (p2 - p1) / dt

    state = np.concatenate([p2, velocity])

    return state.tolist()
