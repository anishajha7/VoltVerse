from flask import Blueprint, request, jsonify
from db import get_connection

bookings_bp = Blueprint('bookings', __name__)

ALL_SLOTS = [
    '09:00', '10:00', '11:00', '12:00', '13:00',
    '14:00', '15:00', '16:00', '17:00', '18:00'
]


@bookings_bp.route('/available', methods=['GET'])
def available_slots():
    station_id = request.args.get('station_id')
    date = request.args.get('date')

    if not station_id or not date:
        return jsonify({"error": "station_id aur date dono chahiye"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT slot_time::text FROM bookings
        WHERE station_id = %s AND slot_date = %s AND status = 'confirmed'
    """, (station_id, date))
    booked = [r[0][:5] for r in cur.fetchall()]
    cur.close()
    conn.close()

    available = [s for s in ALL_SLOTS if s not in booked]
    return jsonify({
        "station_id": station_id,
        "date": date,
        "available": available,
        "booked": booked
    })


@bookings_bp.route('/', methods=['POST'])
def create_booking():
    data = request.json
    required = ['user_id', 'station_id', 'slot_date', 'slot_time']
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} missing hai"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Price calculate karo
    cur.execute("SELECT price_per_hour FROM stations WHERE id = %s", (data['station_id'],))
    row = cur.fetchone()
    if not row:
        return jsonify({"error": "Station not found"}), 404

    price_per_hr = float(row[0])
    duration = data.get('duration_mins', 60)
    total = round(price_per_hr * (duration / 60), 2)

    try:
        cur.execute("""
            INSERT INTO bookings
              (user_id, station_id, slot_date, slot_time, duration_mins, total_price, vehicle_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data['user_id'], data['station_id'], data['slot_date'],
            data['slot_time'], duration, total,
            data.get('vehicle_number', '')
        ))
        booking_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({
            "success": True,
            "booking_id": booking_id,
            "total_price": total,
            "message": f"Booking confirmed! Total: Rs. {total}"
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Yeh slot already booked hai!"}), 409
    finally:
        cur.close()
        conn.close()


@bookings_bp.route('/user/<int:user_id>', methods=['GET'])
def user_bookings(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.id, s.name, s.location, b.slot_date, b.slot_time,
               b.duration_mins, b.total_price, b.status, b.vehicle_number
        FROM bookings b
        JOIN stations s ON b.station_id = s.id
        WHERE b.user_id = %s
        ORDER BY b.slot_date DESC, b.slot_time DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    bookings = []
    for r in rows:
        bookings.append({
            "id": r[0],
            "station_name": r[1],
            "location": r[2],
            "date": str(r[3]),
            "time": str(r[4])[:5],
            "duration_mins": r[5],
            "total_price": float(r[6]),
            "status": r[7],
            "vehicle_number": r[8]
        })
    return jsonify(bookings)


@bookings_bp.route('/<int:booking_id>/cancel', methods=['PATCH'])
def cancel_booking(booking_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE bookings SET status = 'cancelled'
        WHERE id = %s RETURNING id
    """, (booking_id,))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not result:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify({"message": "Booking cancelled successfully"})
