from fastapi import APIRouter
from datetime import datetime
import numpy as np

router = APIRouter()


# ------------------------------------------------
# MOCK ORBIT GENERATORS (REPLACE WITH REAL MODULE 2)
# ------------------------------------------------

def generate_orbit(center_offset=0):

    steps = 120
    orbit = []

    for t in range(steps):
        x = np.cos(t * 0.05) * 7000 + center_offset
        y = np.sin(t * 0.05) * 7000
        z = np.sin(t * 0.02) * 1000
        orbit.append([x, y, z])

    return orbit


def generate_nearby_debris(count=6):

    debris_list = []

    for i in range(count):

        pos = np.random.randn(3) * 500 + np.array([7000, 0, 0])

        debris_list.append({
            "debris_id": f"DEB_{100+i}",
            "position": pos.tolist()
        })

    return debris_list


# ------------------------------------------------
# ENDPOINT
# ------------------------------------------------

@router.get("/visualization/scene/{satellite_id}")
def get_scene_data(satellite_id: str):

    satellite_position = [7000, 0, 0]

    satellite_orbit = generate_orbit()

    debris_objects = generate_nearby_debris()

    debris_orbits = [
        {
            "debris_id": d["debris_id"],
            "orbit": generate_orbit(center_offset=np.random.uniform(-100, 100))
        }
        for d in debris_objects
    ]

    return {
        "satellite_id": satellite_id,
        "generated_at": datetime.utcnow().isoformat(),

        "highlight_object": {
            "type": "satellite",
            "id": satellite_id
        },

        "satellite_positions": [
            {
                "satellite_id": satellite_id,
                "position": satellite_position
            }
        ],

        "debris_positions": debris_objects,

        "orbits": {
            "satellite_orbits": [
                {
                    "satellite_id": satellite_id,
                    "orbit": satellite_orbit
                }
            ],
            "debris_orbits": debris_orbits
        }
    }
