import random
import numpy as np
from datetime import datetime, timedelta

# Temporary satellite storage (replace with real TLE later)
satellite_positions = {
    "ISS": np.array([7000, 0, 0]),
    "SAT_2": np.array([7050, 20, 10]),
    "SAT_3": np.array([7100, -50, 15])
}

DISTANCE_THRESHOLD = 500  # km


def distance(a, b):
    return np.linalg.norm(a - b)


def get_satellite_position(sat_id):
    return satellite_positions.get(sat_id)


def get_nearby_satellites(sat_id):

    base_pos = get_satellite_position(sat_id)
    if base_pos is None:
        return []

    nearby = []

    for other_id, pos in satellite_positions.items():
        if other_id == sat_id:
            continue

        d = distance(base_pos, pos)

        if d < DISTANCE_THRESHOLD:
            nearby.append({
                "satellite_id": other_id,
                "distance_km": float(d),
                "position": pos.tolist()
            })

    return nearby



def get_nearby_debris(satellite_id: int, limit: int = 10):

    debris_list = []

    for _ in range(limit):

        object_id = random.randint(10000, 99999)

        approach_time = datetime.utcnow() + timedelta(
            hours=random.uniform(1, 72)
        )

        debris_list.append({
            "target_satellite_id": satellite_id,
            "object_id": object_id,
            "object_name": f"DEBRIS-{object_id}",
            "distance_km": round(random.uniform(5, 500), 2),
            "relative_velocity_km_s": round(random.uniform(0.5, 15), 2),
            "time_to_approach_hours": round(random.uniform(1, 72), 2),
            "predicted_close_approach_time": approach_time.isoformat(),
            "size_m": round(random.uniform(0.1, 10), 2),
            "risk_score": round(random.uniform(0, 1), 3),
            "direction": random.choice([
                "approaching",
                "receding",
                "crossing_orbit"
            ])
        })

    return debris_list


def get_positions_for_3d(sat_id, satellites_nearby, debris_nearby):

    base_pos = get_satellite_position(sat_id)

    return {
        "main_satellite": base_pos.tolist(),
        "nearby_satellites": [s["position"] for s in satellites_nearby],
        "nearby_debris": [d["position"] for d in debris_nearby]
    }
