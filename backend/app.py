from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, time
import random, math

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Funzione per generare il codice di prenotazione
def generate_unique_code():
    code = str(random.randint(10, 99))
    while Booking.query.filter_by(unique_code=code).first() is not None:
        code = str(random.randint(10, 99))
    return code

# Modello dati per le prenotazioni
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_code = db.Column(db.String(2), unique=True, nullable=False, default=generate_unique_code)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)      
    service_type = db.Column(db.String(10), nullable=False) 
    people = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text, nullable=True)             
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Funzione per calcolare il numero e il tipo di tavoli richiesti 
def compute_required_tables(people):
    if 1 <= people <= 4:
        return {"type": "standard", "tables": 1}
    elif 5 <= people <= 6:
        return {"type": "standard", "tables": 2}
    elif 7 <= people <= 8:
        return {"type": "standard", "tables": 3}
    elif 9 <= people <= 11:
        return {"type": "special", "tables": 1}
    elif 12 <= people <= 15:
        return {"type": "combo", "tables": {"special": 1, "standard": 1}}
    else:
        return None

# Funzione per calcolare i tavoli piccoli già prenotati
def compute_standard_tables_used(booking_date, service_type, exclude_booking_id=None):
    query = Booking.query.filter_by(booking_date=booking_date, service_type=service_type)
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)
    bookings = query.all()
    used = 0
    for b in bookings:
        if 1 <= b.people <= 4:
            used += 1
        elif 5 <= b.people <= 6:
            used += 2
        elif 7 <= b.people <= 8:
            used += 3
        elif 12 <= b.people <= 15:
            used += 1  
    return used

# Funzione per calcolare i tavoli grandi già prenotati
def compute_special_tables_used(booking_date, service_type, exclude_booking_id=None):
    query = Booking.query.filter_by(booking_date=booking_date, service_type=service_type)
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)
    bookings = query.all()
    used = 0
    for b in bookings:
        if 9 <= b.people <= 11:
            used += 1
        elif 12 <= b.people <= 15:
            used += 1  
    return used

with app.app_context():
    db.create_all()

# Endpoint per creare una prenotazione
@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    try:
        first_name = data['first_name']
        last_name = data['last_name']
        phone = data['phone']
        email = data.get('email', None)
        notes = data.get('notes', None)
        service_type = data['service_type'].lower() 
        people = int(data['people'])
        booking_date = datetime.strptime(data['booking_date'], "%Y-%m-%d").date()
        booking_time = datetime.strptime(data['booking_time'], "%H:%M").time()
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except ValueError:
        return jsonify({"error": "Formato dei dati non valido. Assicurati che 'people' sia un numero, 'booking_date' in YYYY-MM-DD e 'booking_time' in HH:MM."}), 400

    # Validazione dell'orario 
    if service_type == "pranzo":
        min_time = time(11, 0)
        max_time = time(15, 30)
        if not (min_time <= booking_time <= max_time):
            return jsonify({"error": "L'orario per il pranzo deve essere tra le 11:00 e le 15:30."}), 400
    elif service_type == "cena":
        min_time = time(18, 0)
        max_time = time(22, 30)
        if not (min_time <= booking_time <= max_time):
            return jsonify({"error": "L'orario per la cena deve essere tra le 18:00 e le 22:30."}), 400

    # Controlla se esiste già una prenotazione per questo cliente 
    existing_booking = Booking.query.filter_by(
        booking_date=booking_date,
        service_type=service_type,
        phone=phone
    ).first()
    if existing_booking:
        return jsonify({"error": "Esiste già una prenotazione per questo cliente per questo giorno e servizio."}), 400

    req = compute_required_tables(people)
    if req is None:
        return jsonify({"error": "Il numero di persone supera il limite gestibile (max 15)."}), 400

    # Controllo disponibilità in base al tipo di tavolo
    if req["type"] == "standard":
        standard_used = compute_standard_tables_used(booking_date, service_type)
        if standard_used + req["tables"] > 40:
            return jsonify({"error": "Non ci sono tavoli standard sufficienti disponibili per questa prenotazione."}), 400
    elif req["type"] == "special":
        special_used = compute_special_tables_used(booking_date, service_type)
        if special_used + req["tables"] > 2:
            return jsonify({"error": "Non ci sono tavoli speciali sufficienti disponibili per questa prenotazione."}), 400
    elif req["type"] == "combo":
        special_used = compute_special_tables_used(booking_date, service_type)
        standard_used = compute_standard_tables_used(booking_date, service_type)
        if special_used + 1 > 2:
            return jsonify({"error": "Non ci sono tavoli speciali sufficienti per questa prenotazione."}), 400
        if standard_used + 1 > 40:
            return jsonify({"error": "Non ci sono tavoli standard sufficienti per questa prenotazione."}), 400

    booking = Booking(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        service_type=service_type,
        people=people,
        booking_date=booking_date,
        booking_time=booking_time,
        notes=notes
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Prenotazione creata con successo",
        "booking": {
            "unique_code": booking.unique_code,
            "first_name": booking.first_name,
            "last_name": booking.last_name,
            "phone": booking.phone,
            "email": booking.email,
            "service_type": booking.service_type,
            "people": booking.people,
            "booking_date": booking.booking_date.strftime("%Y-%m-%d"),
            "booking_time": booking.booking_time.strftime("%H:%M"),
            "tables_reserved": req["tables"],
            "table_type": req["type"],
            "notes": booking.notes
        }
    }), 201

# Endpoint per recuperare una prenotazione tramite codice univoco
@app.route('/bookings/<string:unique_code>', methods=['GET'], endpoint='get_booking_by_code')
def get_booking_by_code(unique_code):
    booking = Booking.query.filter_by(unique_code=unique_code).first()
    if not booking:
        return jsonify({"error": "Prenotazione non trovata"}), 404

    return jsonify({
        "unique_code": booking.unique_code,
        "first_name": booking.first_name,
        "last_name": booking.last_name,
        "phone": booking.phone,
        "email": booking.email,
        "service_type": booking.service_type,
        "people": booking.people,
        "booking_date": booking.booking_date.strftime("%Y-%m-%d"),
        "booking_time": booking.booking_time.strftime("%H:%M"),
        "notes": booking.notes
    }), 200

# Endpoint per recuperare prenotazioni tramite i dati inseriti in prenotazione (query string)
@app.route('/bookings', methods=['GET'])
def get_bookings():
    code = request.args.get('unique_code')
    if code:
        return get_booking_by_code(code)

    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    phone = request.args.get('phone')
    booking_date = request.args.get('booking_date')
    service_type = request.args.get('service_type')

    query = Booking.query
    if first_name:
        query = query.filter(Booking.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Booking.last_name.ilike(f"%{last_name}%"))
    if phone:
        query = query.filter(Booking.phone.ilike(f"%{phone}%"))
    if booking_date:
        try:
            date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            query = query.filter_by(booking_date=date_obj)
        except ValueError:
            return jsonify({"error": "Formato data non valido. Usa YYYY-MM-DD."}), 400
    if service_type:
        query = query.filter_by(service_type=service_type.lower())

    bookings = query.all()
    result = []
    for b in bookings:
        result.append({
            "unique_code": b.unique_code,
            "first_name": b.first_name,
            "last_name": b.last_name,
            "phone": b.phone,
            "email": b.email,
            "service_type": b.service_type,
            "people": b.people,
            "booking_date": b.booking_date.strftime("%Y-%m-%d"),
            "booking_time": b.booking_time.strftime("%H:%M"),
            "notes": b.notes
        })
    return jsonify(result), 200

# Endpoint per cancellare una prenotazione tramite codice univoco
@app.route('/bookings/<string:unique_code>', methods=['DELETE'], endpoint='delete_booking_endpoint')
def delete_booking(unique_code):
    booking = Booking.query.filter_by(unique_code=unique_code).first()
    if not booking:
        return jsonify({"error": "Prenotazione non trovata"}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Prenotazione cancellata con successo"}), 200

# Endpoint per modificare una prenotazione 
@app.route('/bookings/<string:unique_code>', methods=['PUT'], endpoint='update_booking')
def update_booking(unique_code):
    booking = Booking.query.filter_by(unique_code=unique_code).first()
    if not booking:
        return jsonify({"error": "Prenotazione non trovata"}), 404

    data = request.get_json()
    try:
        first_name = data.get('first_name', booking.first_name)
        last_name = data.get('last_name', booking.last_name)
        phone = data.get('phone', booking.phone)
        email = data.get('email', booking.email)
        service_type = data.get('service_type', booking.service_type).lower()
        people = int(data.get('people', booking.people))
        booking_date = datetime.strptime(data.get('booking_date', booking.booking_date.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
        booking_time = datetime.strptime(data.get('booking_time', booking.booking_time.strftime("%H:%M")), "%H:%M").time()
        notes = data.get('notes', booking.notes)
    except ValueError:
        return jsonify({"error": "Formato dei dati non valido. Assicurati che 'people' sia un numero, 'booking_date' in YYYY-MM-DD e 'booking_time' in HH:MM."}), 400

    if service_type == "pranzo":
        min_time = time(11, 0)
        max_time = time(15, 30)
        if not (min_time <= booking_time <= max_time):
            return jsonify({"error": "L'orario per il pranzo deve essere tra le 11:00 e le 15:30."}), 400
    elif service_type == "cena":
        min_time = time(18, 0)
        max_time = time(22, 30)
        if not (min_time <= booking_time <= max_time):
            return jsonify({"error": "L'orario per la cena deve essere tra le 18:00 e le 22:30."}), 400

    existing_booking = Booking.query.filter_by(
        booking_date=booking_date,
        service_type=service_type,
        phone=phone
    ).filter(Booking.id != booking.id).first()
    if existing_booking:
        return jsonify({"error": "Esiste già una prenotazione per questo cliente per questo giorno e servizio."}), 400

    req = compute_required_tables(people)
    if req is None:
        return jsonify({"error": "Il numero di persone supera il limite gestibile (max 15)."}), 400

    if req["type"] == "standard":
        standard_used = compute_standard_tables_used(booking_date, service_type, exclude_booking_id=booking.id)
        if standard_used + req["tables"] > 40:
            return jsonify({"error": "Non ci sono tavoli standard sufficienti disponibili per questa modifica."}), 400
    elif req["type"] == "special":
        special_used = compute_special_tables_used(booking_date, service_type, exclude_booking_id=booking.id)
        if special_used + req["tables"] > 2:
            return jsonify({"error": "Non ci sono tavoli speciali sufficienti disponibili per questa modifica."}), 400
    elif req["type"] == "combo":
        special_used = compute_special_tables_used(booking_date, service_type, exclude_booking_id=booking.id)
        standard_used = compute_standard_tables_used(booking_date, service_type, exclude_booking_id=booking.id)
        if special_used + 1 > 2:
            return jsonify({"error": "Non ci sono tavoli speciali sufficienti per questa prenotazione combo."}), 400
        if standard_used + 1 > 40:
            return jsonify({"error": "Non ci sono tavoli standard sufficienti per questa prenotazione combo."}), 400

    booking.first_name = first_name
    booking.last_name = last_name
    booking.phone = phone
    booking.email = email
    booking.service_type = service_type
    booking.people = people
    booking.booking_date = booking_date
    booking.booking_time = booking_time
    booking.notes = notes

    db.session.commit()

    return jsonify({
        "message": "Prenotazione aggiornata con successo",
        "booking": {
            "unique_code": booking.unique_code,
            "first_name": booking.first_name,
            "last_name": booking.last_name,
            "phone": booking.phone,
            "email": booking.email,
            "service_type": booking.service_type,
            "people": booking.people,
            "booking_date": booking.booking_date.strftime("%Y-%m-%d"),
            "booking_time": booking.booking_time.strftime("%H:%M"),
            "notes": booking.notes
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
