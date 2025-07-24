from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="postgres_db",
    database="hotel_db",
    user="admin",
    password="admin"
)


@app.route("/chambres", methods=["GET"])
def get_chambres():
    cur = conn.cursor()
    cur.execute("SELECT * FROM rooms;")
    rows = cur.fetchall()
    result = [{"id": r[0], "number": r[1], "type": r[2], "price_per_night": r[4]} for r in rows]
    cur.close()
    return jsonify(result)


@app.route("/reservations", methods=["POST"])
def create_reservation():
    data = request.json
    room_id = data.get("room_id")
    user_id = data.get("user_id")
    check_in_date = data.get("check_in_date")
    check_out_date = data.get("check_out_date")

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reservations (user_id, room_id, check_in_date, check_out_date)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (user_id, room_id, check_in_date, check_out_date))
    reservation_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"message": "Réservation créée", "id": reservation_id}), 201


@app.route("/reservations/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
    conn.commit()
    cur.close()
    return jsonify({"message": f"Réservation {reservation_id} supprimée"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
