#   🐍REST API на Python

* **📓Описание**

    Простое API, реализовано под взаимодействие с базой данных PostgreSQL, с использованим Flask и SQLAlchemy.
    Поддерживает запросы CRUD.


* **💻Настройка бд:**

   Postgres должен иметь стандартные настройки пользователя, пароля и порта.
   
   *    user = postgres
   *    passwd = 1111
   *    port = 5432
   

   Для работы API необходимо создать базу данных "test_dealer", и импортировать заготовленный файл "simple_cars_list.sql".

   ```
   $psql
   postgres=# create database test_dealer;
   postgres=# \c test_dealer;
   postgres=# \i $PATH/simple_cars_list.sql;
   ```


* **✴️URL**

  <_127.1:5000/dealer_>
  <_127.1:5000/dealer/(int)_> 

* **📮Типы запросов:**

  `GET` | `POST` | `DELETE` | `PUT`

* **Метод `GET` для `/dealer`**
 
    ```python
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
    ```
    Возвращает все записи из базы данных в формете JSON и <b>status_code == 200</b>
    ```JSON
    [{
        "date": 2005,
        "id": 1,
        "mileage_km": 7641,
        "model": "S40",
        "power_hp": 119,
        "price_rub": 1879793,
        "producer": "Volvo"
    },
    {
        "date": 2008,
        "id": 2,
        "mileage_km": 21052,
        "model": "Santa Fe",
        "power_hp": 120,
        "price_rub": 1024972,
        "producer": "Hyundai"
    }]
    ```   

* **Метод `POST` для `/dealer`**
 
    ```python
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
            price_rub=data['price_rub'])
        db.session.add(new_car)
        db.session.commit()
        return {'message': f'car {new_car.producer, new_car.model} has been created successfully.'}
    else:
        return {'error': 'The request payload is not in JSON format'}
    ```
    Получает reqest в формате JSON
    ```JSON
    {
        "date": 2020, 
        "mileage_km": 70, 
        "model": "Turbo S", 
        "power_hp": 500, 
        "price_rub": 2500000, 
        "producer": "Porshe"
    }
    ```
    
    При успешном добавлении элемента в бд, возвращает сообщение и <b>status_code == 200</b>
    ```JSON
    {
        "message": "car ('Porshe', 'Turbo S') has been created  successfully."
    }
    ```

    При неудачной попытке добавить элемент, вернет сообщение и <b>status_code == 400</b>

* **Методы `GET` | `PUT` | `DELETE` для `/dealer/<car_id>`**
Реализованы в одном месте, т.к. все они направленны на работу с одним единственным элементом.
 
    ```python
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
    ```

    *   `GET` Возвращает элемент по его `id` в формате JSON 
    
        <b>status_code == 200</b>
        ```JSON
        {
            "date": 2000,
            "id": 34,
            "mileage_km": 16942,
            "model": "Vitara",
            "power_hp": 176,
            "price_rub": 1089705,
            "producer": "Suzuki"
        }
        ```

    *   `PUT` Получает reqest в формате JSON на изменение элемента в бд по  его `id`. Возвращает сообщение и <b>status_code == 200</b>
        *   Было 
            ```JSON
            {
                "date": 1960,
                "id": 51,
                "mileage_km": 19224,
                "model": "Corvair",
                "power_hp": 127,
                "price_rub": 1526523,
                "producer": "Chevrolet"
            }
            ```
        *   Отправляем reqest `PUT` в формате JSON
            ```JSON
            {
                "date": 1960,
                "mileage_km": 19224,
                "model": "Corvair",
                "power_hp": 523,
                "price_rub": 2600000,
                "producer": "Chevrolet"
            }
            ```
        *   Получили ответ

            <b>status_code == 200</b> и сообщение           
            ```JSON
            {
                "message": "car ('Chevrolet', 'Corvair') successfully updated"
            }
            ``` 

        *   Стало
            ```JSON
            {
                "date": 1960,
                "id": 51,
                "mileage_km": 19224,
                "model": "Corvair",
                "power_hp": 523,
                "price_rub": 2600000,
                "producer": "Chevrolet"
            }
            ```

        * В случае ошибки вернет <b>status_code == 400</b>

    * `DELETE` удаляет элемент из таблицы по его `id`

        Возвращает сообщение в формате JSON и <b>status_code == 200</b>
        ```JSON
        {
            "message": "Car ('Porshe', 'Turbo S') successfully deleted."
        }
        ```
        В случае ошибок вернет <b>status_code == 400</b>
