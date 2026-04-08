from backend.loader import load_stops
from backend.gtfs_live import fetch_live_positions

stops = load_stops()

def get_stop_markers(limit=20):
    markers = []
    for sid, s in list(stops.items())[:limit]:
        markers.append({
            "id": sid,
            "lat": s["lat"],
            "lon": s["lon"],
            "label": s["name"]["en"]
        })
    return markers

def get_live_bus_markers():
    data = fetch_live_positions()
    markers = []
    if "entity" in data:  # GTFS-Realtime format
        for e in data["entity"]:
            vp = e.get("vehicle", {}).get("position", {})
            if vp:
                markers.append({
                    "lat": vp.get("latitude"),
                    "lon": vp.get("longitude"),
                    "label": e.get("vehicle", {}).get("trip", {}).get("route_id", "bus")
                })
    return markers
