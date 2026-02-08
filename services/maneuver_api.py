from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
from datetime import datetime

router = APIRouter()


# ------------------------------------------------
# REQUEST MODEL
# ------------------------------------------------

class ManeuverRequest(BaseModel):
    satellite_id: str
    debris_id: str


# ------------------------------------------------
# MOCK ENGINE LOGIC
# ------------------------------------------------

def choose_maneuver():

    types = [
        "RADIAL_OUT",
        "PROGRADE_BURN",
        "PLANE_CHANGE"
    ]

    return np.random.choice(types)


def estimate_delta_v():
    return np.random.uniform(0.2, 2.0)


def estimate_fuel_cost(delta_v):
    return delta_v * 0.9


def predict_new_orbit():

    steps = 120
    orbit = np.cumsum(np.random.randn(steps, 3), axis=0)
    return orbit.tolist()


# ------------------------------------------------
# ENDPOINT
# ------------------------------------------------

@router.post("/maneuver/calculate")
def calculate_maneuver(req: ManeuverRequest):

    maneuver = choose_maneuver()

    delta_v = estimate_delta_v()

    fuel = estimate_fuel_cost(delta_v)

    orbit = predict_new_orbit()

    return {
        "satellite_id": req.satellite_id,
        "debris_id": req.debris_id,
        "generated_at": datetime.utcnow().isoformat(),

        "recommended_maneuver_type": maneuver,
        "delta_v_required": float(delta_v),
        "fuel_cost_kg": float(fuel),

        "new_orbit_prediction": orbit
    }
