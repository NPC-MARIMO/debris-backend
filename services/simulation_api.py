from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
from datetime import datetime

router = APIRouter()


# ------------------------------------------------
# REQUEST MODEL
# ------------------------------------------------

class WhatIfRequest(BaseModel):
    satellite_id: str
    debris_id: str
    maneuver_type: str
    delta_v: float
    time_shift: float


# ------------------------------------------------
# MOCK PHYSICS FUNCTIONS (REPLACE LATER)
# ------------------------------------------------

def mock_current_probability():
    return np.random.uniform(0.3, 0.8)


def apply_mock_maneuver(probability, delta_v, time_shift):

    reduction_factor = min(delta_v * 0.05 + time_shift * 0.001, 0.8)

    new_prob = max(probability * (1 - reduction_factor), 0.0001)

    return new_prob


def mock_new_trajectory():

    steps = 120
    traj = np.cumsum(np.random.randn(steps, 3), axis=0)
    return traj.tolist()


def estimate_fuel(delta_v):
    return delta_v * 0.8


# ------------------------------------------------
# ENDPOINT
# ------------------------------------------------

@router.post("/simulation/what-if")
def run_what_if_simulation(req: WhatIfRequest):

    current_prob = mock_current_probability()

    new_prob = apply_mock_maneuver(
        current_prob,
        req.delta_v,
        req.time_shift
    )

    new_traj = mock_new_trajectory()

    fuel = estimate_fuel(req.delta_v)

    risk_reduction = current_prob - new_prob

    return {
        "satellite_id": req.satellite_id,
        "debris_id": req.debris_id,
        "generated_at": datetime.utcnow().isoformat(),

        "original_probability": float(current_prob),
        "new_collision_probability": float(new_prob),

        "risk_reduction": float(risk_reduction),

        "fuel_estimate_kg": float(fuel),

        "new_trajectory": new_traj
    }
