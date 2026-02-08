from services.catalog_service import catalog
import random
import requests

TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"


def load_satellites():

    response = requests.get(TLE_URL, timeout=20)
    response.raise_for_status()

    lines = response.text.strip().split("\n")

    satellites = []

    # TLE format = 3 lines per satellite
    for i in range(0, len(lines), 3):
        try:
            name = lines[i].strip()
            line1 = lines[i + 1].strip()
            line2 = lines[i + 2].strip()

            satellites.append({
                "satellite_id": name,   # using name as ID
                "tle1": line1,
                "tle2": line2
            })

        except IndexError:
            continue
    print(satellites)
    return satellites


def get_satellite_info(satellite_id):
    allsatellites = load_satellites()
    print(f"Total satellites loaded: {len(allsatellites)}")
    for sat in allsatellites:
        if sat["satellite_id"] == satellite_id:
            print(f" {satellite_id}")
            return sat

def get_nearby_debris(satellite_id):

    debris_list = []
 
    for object_id in catalog.keys():
        if catalog[object_id].get("associated_satellite") == satellite_id:
            debris_list.append({
                "object_id": object_id,
                "distance_km": round(random.uniform(5, 500), 2),
                "risk_level": random.choice(["LOW", "MEDIUM", "HIGH"])
            })

    return debris_list


def get_collision_summary():

    return {
        "total_risky_objects": random.randint(0, 5),
        "highest_risk_object": "DEB_1",
        "closest_approach_km": round(random.uniform(1, 50), 2)
    }


def get_alerts():

    alerts = []

    if random.random() > 0.5:
        alerts.append({
            "type": "HIGH_RISK_COLLISION",
            "message": "Debris predicted close approach"
        })

    return alerts


def get_risk_counts(debris_list):

    counts = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0
    }

    for d in debris_list:
        risk = d.get("risk_level")

        if risk in counts:
            counts[risk] += 1

    return counts
