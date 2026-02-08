from fastapi import APIRouter
from datetime import datetime
import numpy as np

router = APIRouter()


# ------------------------------------------------
# MOCK ALERT ENGINE (REPLACE WITH REAL COLLISION PIPELINE)
# ------------------------------------------------

def generate_mock_alerts(satellite_id):

    alert_levels = ["CRITICAL", "HIGH", "MEDIUM"]

    alerts = []

    for i in range(np.random.randint(2, 6)):

        level = np.random.choice(alert_levels)

        alerts.append({
            "alert_id": f"ALT_{np.random.randint(1000,9999)}",
            "satellite_id": satellite_id,
            "debris_id": f"DEB_{np.random.randint(100,999)}",
            "risk_level": level,
            "probability": float(np.random.uniform(0.2, 0.9)),
            "message": f"{level} collision risk detected"
        })

    return alerts


# ------------------------------------------------
# HELPER
# ------------------------------------------------

def split_alerts(alerts):

    critical = []
    active = []

    for a in alerts:

        active.append(a)

        if a["risk_level"] == "CRITICAL":
            critical.append(a)

    return active, critical


# ------------------------------------------------
# ENDPOINT
# ------------------------------------------------

@router.get("/alerts/{satellite_id}")
def get_alerts(satellite_id: str):

    raw_alerts = generate_mock_alerts(satellite_id)

    active_alerts, critical_alerts = split_alerts(raw_alerts)

    return {
        "satellite_id": satellite_id,
        "generated_at": datetime.utcnow().isoformat(),

        "active_alerts": active_alerts,
        "critical_alerts": critical_alerts,

        "timestamps": {
            "generated_at": datetime.utcnow().isoformat(),
            "next_refresh_suggested": 10
        }
    }
