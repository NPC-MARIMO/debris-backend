from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


# ------------------------------------------------
# REQUEST MODELS
# ------------------------------------------------

class SatelliteInfo(BaseModel):
    satellite_id: str
    orbit_type: str | None = None


class DebrisInfo(BaseModel):
    debris_id: str
    size_m: float | None = None


class CollisionData(BaseModel):
    probability: float
    closest_distance_km: float
    relative_velocity_km_s: float
    tca_seconds: float


class AIRiskRequest(BaseModel):
    satellite: SatelliteInfo
    debris: DebrisInfo
    collision_data: CollisionData


# ------------------------------------------------
# RULE BASED EXPLANATION ENGINE (REPLACE WITH GEMINI LATER)
# ------------------------------------------------

def generate_explanation(data: CollisionData):

    prob = data.probability
    dist = data.closest_distance_km
    vel = data.relative_velocity_km_s

    if prob > 0.6:
        level = "critical"
    elif prob > 0.3:
        level = "high"
    elif prob > 0.1:
        level = "medium"
    else:
        level = "low"

    explanation = (
        f"Collision probability is {prob:.2f}. "
        f"Closest approach distance is {dist:.2f} km. "
        f"Relative velocity is {vel:.2f} km/s. "
        f"This scenario is classified as {level} risk."
    )

    return explanation, level


def recommend_action(level):

    if level == "critical":
        return "Immediate maneuver strongly recommended."

    if level == "high":
        return "Maneuver planning recommended within next orbit window."

    if level == "medium":
        return "Continue monitoring. Prepare contingency maneuver."

    return "No maneuver required. Continue tracking."


def reasoning_text(level, data):

    return (
        f"Risk level determined using probability {data.probability:.2f}, "
        f"distance {data.closest_distance_km:.2f} km and velocity "
        f"{data.relative_velocity_km_s:.2f} km/s."
    )


# ------------------------------------------------
# ENDPOINT
# ------------------------------------------------

@router.post("/ai/risk-insight")
def ai_risk_insight(req: AIRiskRequest):

    explanation, level = generate_explanation(req.collision_data)

    action = recommend_action(level)

    reasoning = reasoning_text(level, req.collision_data)

    return {
        "satellite_id": req.satellite.satellite_id,
        "debris_id": req.debris.debris_id,
        "generated_at": datetime.utcnow().isoformat(),

        "human_readable_explanation": explanation,
        "recommended_action": action,
        "risk_reasoning": reasoning
    }
