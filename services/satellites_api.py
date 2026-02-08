from fastapi import APIRouter, Query
import requests
from datetime import datetime

router = APIRouter()

TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"


def load_satellites():
    try:
        response = requests.get(TLE_URL, timeout=20)
        response.raise_for_status()
        return response.text.strip().splitlines()
    except Exception as e:
        print("TLE FETCH FAILED:", e)
        return []


@router.get("/satellites/tle")
def get_satellites(limit: int = Query(default=100)):

    tle_lines = load_satellites()

    results = []

    # Step in blocks of 3 lines (name, line1, line2)
    for i in range(0, min(len(tle_lines), limit * 3), 3):

        try:
            name = tle_lines[i].strip()
            line1 = tle_lines[i + 1]

            norad_id = int(line1[2:7])

            results.append({
                "satellite_name": name,
                "satellite_id": norad_id
            })

        except:
            continue

    return {
        "source": "celestrak_active",
        "generated_at": datetime.utcnow().isoformat(),
        "total_lines_loaded": len(tle_lines),
        "returned": len(results),
        "satellites": results
    }
