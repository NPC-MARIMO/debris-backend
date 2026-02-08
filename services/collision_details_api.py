from fastapi import APIRouter, Query
from datetime import datetime
import numpy as np

router = APIRouter()


# ------------------------------------------------
# MOCK ENGINE FUNCTIONS (REPLACE LATER)
# ------------------------------------------------

def get_pair_orbit_data(satellite_id: str, debris_id: str):

    # Replace with real Module 2 + Module 3 outputs

    steps = 100

    sat_orbit = np.random.rand(steps, 3) * 10000
    debris_orbit = sat_orbit + np.random.randn(steps, 3) * 2

    return sat_orbit, debris_orbit


def compute_distances(sat_orbit, debris_orbit):
    return np.linalg.norm(sat_orbit - debris_orbit, axis=1)


def compute_probability(distance):
    sigma = 2.5
    return float(np.exp(-(distance**2)/(2*sigma**2)))


# ------------------------------------------------
# MAIN ENDPOINT
# ------------------------------------------------

@router.get("/collision/details")
def collision_details(
    satellite_id: str = Query(...),
    debris_id: str = Query(...)
):

    sat_orbit, debris_orbit = get_pair_orbit_data(
        satellite_id,
        debris_id
    )

    distances = compute_distances(sat_orbit, debris_orbit)

    min_idx = int(np.argmin(distances))
    closest_distance = float(distances[min_idx])

    probability = compute_probability(closest_distance)

    # Relative velocity approx
    if min_idx > 0:
        vel = np.linalg.norm(
            (sat_orbit[min_idx] - sat_orbit[min_idx-1]) -
            (debris_orbit[min_idx] - debris_orbit[min_idx-1])
        )
    else:
        vel = 0.0

    # Relative trajectory for visualization
    relative_trajectory = (
        debris_orbit - sat_orbit
    ).tolist()

    timeline_data = []

    for i in range(len(distances)):
        timeline_data.append({
            "time_step": i,
            "distance_km": float(distances[i]),
            "probability": compute_probability(distances[i])
        })

    response = {
        "satellite_id": satellite_id,
        "debris_id": debris_id,

        "generated_at": datetime.utcnow().isoformat(),

        "closest_distance_km": closest_distance,
        "collision_probability": probability,
        "relative_velocity_km_s": float(vel),

        "relative_trajectory": relative_trajectory,
        "timeline_data": timeline_data
    }

    return response
