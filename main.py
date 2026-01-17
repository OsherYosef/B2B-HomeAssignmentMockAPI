from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone
import random

app = FastAPI(
    title="Mock Drone Sensor Systems",
    description="Mock APIs for Drone Detection Systems A & B",
    version="1.0.0"
)

# ------------------------
# Utility
# ------------------------

def now_epoch() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def jitter(value: float, delta: float = 0.0005) -> float:
    return value + random.uniform(-delta, delta)


# ------------------------
# Dataset
# ------------------------

BASE_DRONES = [
    {
        "id": "DRN-1",
        "lat": 32.0853,
        "lon": 34.7818,
        "alt": 120.0,
        "model": "DJI Mini 3",
        "manufacturer": "DJI"
    },
    {
        "id": "DRN-2",
        "lat": 32.0861,
        "lon": 34.7825,
        "alt": 98.0,
        "model": "DJI Air 2",
        "manufacturer": "DJI"
    },
    {
        "id": "DRN-3",
        "lat": 32.0847,
        "lon": 34.7809,
        "alt": 150.0,
        "model": "Autel Evo",
        "manufacturer": "Autel"
    },
    {
        "id": "DRN-4",
        "lat": 32.0870,
        "lon": 34.7831,
        "alt": 110.0,
        "model": "Parrot Anafi",
        "manufacturer": "Parrot"
    },
    {
        "id": "DRN-5",
        "lat": 32.0839,
        "lon": 34.7798,
        "alt": 130.0,
        "model": "DJI Mini 2",
        "manufacturer": "DJI"
    }
]

# ------------------------
# System A schema
# ------------------------

class SystemAResponse(BaseModel):
    drone_id: str
    timestamp: int
    Location_lat: float
    Location_lon: float
    Locatin_alt: float = Field(..., description="Typo is intentional")
    drone_model: str


# ------------------------
# System B schema
# ------------------------

class GeoJSONPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float]  # [lon, lat, alt]


class SystemBResponse(BaseModel):
    Serial: str
    Detection_timestamp: str
    Location: GeoJSONPoint
    type: str
    Model: str
    manufacturer: str


# ------------------------
# Endpoints
# ------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get(
    "/system-a/detections",
    response_model=List[SystemAResponse],
    summary="System A – Drone detections"
)
def get_system_a_detections():
    """
    Simulates detections from System A.
    Timestamp and location change on every request.
    """
    responses = []

    for drone in BASE_DRONES:
        responses.append(SystemAResponse(
            drone_id=f"A-{drone['id']}",
            timestamp=now_epoch(),
            Location_lat=jitter(drone["lat"]),
            Location_lon=jitter(drone["lon"]),
            Locatin_alt=drone["alt"] + random.uniform(-5, 5),
            drone_model=drone["model"]
        ))

    return responses


@app.get(
    "/system-b/detections",
    response_model=List[SystemBResponse],
    summary="System B – Drone detections"
)
def get_system_b_detections():
    """
    Simulates detections from System B using GeoJSON and ISO timestamps.
    """
    responses = []

    for drone in BASE_DRONES:
        responses.append(SystemBResponse(
            Serial=f"SN-{drone['id']}",
            Detection_timestamp=now_iso(),
            Location=GeoJSONPoint(
                coordinates=[
                    jitter(drone["lon"]),
                    jitter(drone["lat"]),
                    drone["alt"] + random.uniform(-5, 5)
                ]
            ),
            type="UAV",
            Model=drone["model"].split()[-1],
            manufacturer=drone["manufacturer"]
        ))

    return responses
