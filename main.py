from fastapi import FastAPI, File, UploadFile
from polars import datetime
from services.detection_service import detect_debris
from services.catalog_service import add_observation, get_object_history
from pydantic import BaseModel
from services.state_service import compute_state_vector
from services.dashboard_service import (
    get_satellite_info,
    get_nearby_debris,
    get_collision_summary,
    get_alerts,
    get_risk_counts
)
from services.nearby_service import (
    get_nearby_satellites,
    get_nearby_debris,
    get_positions_for_3d
)
from fastapi import FastAPI
from services.collision_api import router as collision_router

from fastapi import FastAPI
from services.collision_details_api import router as details_router

from fastapi import FastAPI
from services.simulation_api import router as sim_router
from services.maneuver_api import router as maneuver_router
from services.ai_insight_api import router as ai_router
from services.alerts_api import router as alerts_router
from services.visualization_api import router as viz_router
from fastapi.middleware.cors import CORSMiddleware
from services.satellites_api import router as sat_router

app = FastAPI()
app.include_router(sat_router)



# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(viz_router)


app.include_router(ai_router)


app.include_router(alerts_router)



app.include_router(sim_router)
app.include_router(maneuver_router)






app.include_router(details_router)

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/detect-debris")
async def detect(file: UploadFile = File(...)):

    image_bytes = await file.read()

    detections = detect_debris(image_bytes)

    return {
        "detections": detections
    }


class ObservationRequest(BaseModel):
    object_id: str
    pixel_x: float
    pixel_y: float
    timestamp: float

@app.post("/add-observation")
def add_obs(data: ObservationRequest):

    add_observation(
        data.object_id,
        data.pixel_x,
        data.pixel_y,
        data.timestamp
    )

    return {
        "status": "stored",
        "object_id": data.object_id
    }


@app.get("/object-history/{object_id}")
def history(object_id: str):

    history = get_object_history(object_id)

    return {
        "object_id": object_id,
        "observations": history
    }


@app.get("/object-state/{object_id}")
def get_state(object_id: str):

    state = compute_state_vector(object_id)

    if state is None:
        return {
            "error": "Not enough observations"
        }

    return {
        "object_id": object_id,
        "state_vector": state
    }


@app.get("/dashboard/{satellite_id}")
def dashboard(satellite_id: str):

    satellite_info = get_satellite_info(satellite_id)

    nearby_debris = get_nearby_debris(satellite_id)

    collision_summary = get_collision_summary()

    alerts = get_alerts()

    risk_counts = get_risk_counts(nearby_debris)

    return {
        "satellite_info": satellite_info,
        "nearby_debris_list": nearby_debris,
        "collision_summary": collision_summary,
        "alerts": alerts,
        "risk_counts": risk_counts
    }


@app.get("/satellite/{sat_id}/nearby-objects")
def nearby_debris(satellite_id: int):

    debris = get_nearby_debris(satellite_id)

    return {
        "satellite_id": satellite_id,
        "generated_at": datetime.utcnow().isoformat(),
        "objects_found": len(debris),
        "debris_objects": debris
    }

app.include_router(collision_router)

