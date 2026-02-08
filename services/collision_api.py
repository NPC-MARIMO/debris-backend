from fastapi import APIRouter, Query
from datetime import datetime
from typing import List, Dict

router = APIRouter()

# ---- MOCK DATABASE / SERVICE IMPORTS ----
# Replace with your real imports later
# from services.collision_service import get_collision_risks_for_satellite


# ------------------------------------------------
# MOCK SERVICE FUNCTION (REMOVE LATER)
# ------------------------------------------------

def get_collision_risks_for_satellite(satellite_id: str):

    # Replace with real engine output
    return [
        {
            "debris_id": "DEB_9912",
            "probability": 0.72,
            "risk_level": "CRITICAL",
            "tca_seconds": 1420,
            "closest_distance_km": 1.8,
            "relative_velocity_km_s": 12.4
        },
        {
            "debris_id": "DEB_5531",
            "probability": 0.41,
            "risk_level": "HIGH",
            "tca_seconds": 2200,
            "closest_distance_km": 4.5,
            "relative_velocity_km_s": 10.1
        }
    ]


# ------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------

def build_risk_summary(objects: List[Dict]):

    summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for obj in objects:
        level = obj["risk_level"].lower()
        if level in summary:
            summary[level] += 1

    return summary


def should_recommend_action(risk_level: str):
    return risk_level in ["CRITICAL", "HIGH"]


# ------------------------------------------------
# MAIN API ENDPOINT
# ------------------------------------------------

@router.get("/satellite/{satellite_id}/collision-risks")
def get_collision_risks(
    satellite_id: str,
    min_risk: str = Query(default="low"),
    limit: int = Query(default=50)
):

    raw_data = get_collision_risks_for_satellite(satellite_id)

    # Risk filter
    risk_order = ["low", "medium", "high", "critical"]
    min_index = risk_order.index(min_risk.lower())

    filtered = [
        obj for obj in raw_data
        if risk_order.index(obj["risk_level"].lower()) >= min_index
    ]

    # Sort
    filtered.sort(
        key=lambda x: (
            risk_order.index(x["risk_level"].lower()),
            -x["probability"]
        ),
        reverse=True
    )

    # Limit
    filtered = filtered[:limit]

    # Add computed fields
    final_objects = []
    for obj in filtered:

        final_objects.append({
            **obj,
            "recommended_action": should_recommend_action(obj["risk_level"]),
            "tca_timestamp": datetime.utcnow().isoformat()
        })

    response = {
        "satellite_id": satellite_id,
        "generated_at": datetime.utcnow().isoformat(),
        "risk_summary": build_risk_summary(final_objects),
        "collision_objects": final_objects
    }

    return response
