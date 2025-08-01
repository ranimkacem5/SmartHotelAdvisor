from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Connexion unique à PostgreSQL
conn = psycopg2.connect(
    host="postgres_db",
    database="hotel_db",
    user="admin",
    password="admin"
)


@app.route("/rooms", methods=["GET"])
def get_rooms():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, number, type, capacity, price_per_night, amenities, is_available FROM rooms")
        rooms = cur.fetchall()
        cur.close()

        result = []
        for r in rooms:
            room = {
                "id": r[0],
                "number": r[1],
                "type": r[2],
                "capacity": r[3],
                "price_per_night": float(r[4]) if r[4] is not None else None,
                "amenities": r[5],
                "is_available": r[6]
            }
            result.append(room)
        return jsonify(result), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/rooms", methods=["POST"])
def create_room():
    data = request.json
    required_fields = ["number"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Champs manquants : {', '.join(missing)}"}), 400

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO rooms (number, type, capacity, price_per_night, amenities, is_available)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (data["number"], data.get("type"), data.get("capacity"), data.get("price_per_night"),
              data.get("amenities"), data.get("is_available", True)))

        room_id = cur.fetchone()[0]
        conn.commit()
        cur.close()

        return jsonify({"message": "Chambre créée", "id": room_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/rooms/<int:room_id>/images", methods=["GET"])
def get_room_images(room_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, image_url FROM room_images WHERE room_id = %s", (room_id,))
        images = cur.fetchall()
        cur.close()

        result = [{"id": img[0], "image_url": img[1]} for img in images]
        return jsonify(result), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/rooms/<int:room_id>/images", methods=["POST"])
def add_room_image(room_id):
    data = request.json
    image_url = data.get("image_url")
    if not image_url:
        return jsonify({"error": "Champ 'image_url' manquant"}), 400

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO room_images (room_id, image_url) VALUES (%s, %s) RETURNING id", (room_id, image_url))
        image_id = cur.fetchone()[0]
        conn.commit()
        cur.close()

        return jsonify({"message": "Image ajoutée", "id": image_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/reservations", methods=["POST"])
def create_reservation():
    data = request.json
    required_fields = ["user_id", "room_id", "check_in_date", "check_out_date"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Champs manquants : {', '.join(missing)}"}), 400

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reservations (user_id, room_id, check_in_date, check_out_date, total_price, payment_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (data["user_id"], data["room_id"], data["check_in_date"], data["check_out_date"],
              data.get("total_price"), data.get("payment_type")))

        reservation_id = cur.fetchone()[0]
        conn.commit()
        cur.close()

        return jsonify({"message": "Réservation créée", "id": reservation_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/reservations/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
        conn.commit()
        cur.close()

        return jsonify({"message": f"Réservation {reservation_id} supprimée"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
