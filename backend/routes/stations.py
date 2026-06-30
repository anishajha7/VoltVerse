from flask import Blueprint, jsonify
from db import get_connection

stations_bp = Blueprint('stations', __name__)


@stations_bp.route('/', methods=['GET'])
def get_all_stations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, location, total_slots, charger_type, price_per_hour
        FROM stations
        WHERE is_active = TRUE
        ORDER BY name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    stations = []
    for r in rows:
        stations.append({
            "id": r[0],
            "name": r[1],
            "location": r[2],
            "total_slots": r[3],
            "charger_type": r[4],
            "price_per_hour": float(r[5])
        })
    return jsonify(stations)


@stations_bp.route('/<int:station_id>', methods=['GET'])
def get_station(station_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, location, total_slots, charger_type, price_per_hour
        FROM stations WHERE id = %s
    """, (station_id,))
    r = cur.fetchone()
    cur.close()
    conn.close()

    if not r:
        return jsonify({"error": "Station not found"}), 404

    return jsonify({
        "id": r[0], "name": r[1], "location": r[2],
        "total_slots": r[3], "charger_type": r[4],
        "price_per_hour": float(r[5])
    })
