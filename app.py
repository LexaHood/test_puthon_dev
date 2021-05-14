from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

client = app.test_client()

#Подключение к базе данных postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@127.1:5432/test_dealer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель таблицы
class Data(db.Model):
    __tablename__ = 'simple_cars_list'

    id = db.Column(db.Integer, primary_key = True)
    producer = db.Column(db.String(50))
    model = db.Column(db.String(50))
    date = db.Column(db.Integer())
    power_hp = db.Column(db.Integer())
    mileage_km = db.Column(db.Integer())
    price_rub = db.Column(db.Integer())

    def __init__(self, producer, model, date, power_hp, mileage_km, price_rub):
        self.producer = producer
        self.model = model
        self.date = date
        self.power_hp = power_hp
        self.mileage_km = mileage_km
        self.price_rub = price_rub

    def __repr__(self):
        return f'<Car {self.producer, self.model}>'


@app.route('/dealer', methods=['GET'])
def get_cars():
    cars = Data.query.all()
    results = [
        {
            'id': car.id,
            'producer': car.producer,
            'model': car.model,
            'date': car.date,
            'power_hp': car.power_hp,
            'mileage_km': car.mileage_km,
            'price_rub': car.price_rub
        } for car in cars]

    return jsonify(results)

@app.route('/dealer', methods=['POST'])
def insert_car():
    if request.is_json:
        data = request.get_json()
        new_car = Data(
            producer=data['producer'], 
            model=data['model'], 
            date=data['date'], 
            power_hp=data['power_hp'],
            mileage_km=data['mileage_km'],
            price_rub=data['price_rub'] 
        )

        db.session.add(new_car)
        db.session.commit()
        return {'message': f'car {new_car.producer, new_car.model} has been created successfully.'}
    else:
        return {'error': 'The request payload is not in JSON format'}

@app.route('/dealer/<car_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(car_id):
    car = Data.query.get_or_404(car_id)

    if request.method == 'GET':
        response = {
            'id': car.id,
            "producer": car.producer,
            "model": car.model,
            "date": car.date,
            'power_hp': car.power_hp,
            'mileage_km': car.mileage_km,
            'price_rub': car.price_rub
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        car.producer = data['producer']
        car.model = data['model']
        car.date = data['date']
        car.power_hp = data['power_hp']
        car.mileage_km = data['mileage_km']
        car.price_rub = data['price_rub']
        db.session.add(car)
        db.session.commit()
        return {'message': f'car {car.producer, car.model} successfully updated'}

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return {'message': f'Car {car.producer, car.model} successfully deleted.'}

if __name__ == "__main__":
    app.run(debug=True)