import json
from flask import Flask, jsonify, request

app = Flask(__name__)

cars = [
    {'id': 1, "name": 'Baleno'},
    {'id':2, "name": 'Thar'},
    {'id':3, "name": "Ertiga"},
    {'id':4, "name":"carens"} 
]
next_car_id = 5

###### GET all cars ###################################

@app.route('/cars',methods=['GET'])
def get_cars():
    return jsonify(cars)


#######################################################

def get_car(id):
    for i in cars:
        if i['id'] == id:
            return i

@app.route('/cars/<int:id>', methods=['GET'])
def get_car_by_id(id):
    car = get_car(id)
    if car is None:
        return jsonify({'error':'car does not exist'}, 404)
    return jsonify(car)

###############################################################

def car_is_valid(car):
    for key in car.keys():
        if key != 'name':
            return False
    return True

def car_already_exist(car):
    for i in cars:
        print(i)
        print(i['name'])
        print(car['name'])
        if i['name'] == car['name']:
            return True
    return False
        
@app.route('/cars', methods=['POST'])
def create_car():
    global next_car_id
    car = json.loads(request.data)
    if not car_is_valid(car):
        return jsonify({'error':'Invalid car properties'}), 400
    
    if car_already_exist(car):
        return jsonify({'error':'car already exists'}), 400
    
    car['id'] = next_car_id

    next_car_id += 1
    cars.append(car)
    return '', 201, {'location': f"/cars"}

###################################################################

@app.route('/cars/<int:id>',methods=['PUT'])
def update_car(id):
    car = get_car(id)
    if car is None:
        return jsonify({'error':'cars does not exist'}), 404
    updated_car = json.loads(request.data)
    if not car_is_valid(updated_car):
        return jsonify(
            {
            'error': "invalid car properties"
            },
            400
        )
        
    if car_already_exist(updated_car):
        return jsonify({'error':'car already exists'}), 400

    car.update(updated_car)
    return jsonify(car)

####################################################################

@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_employee(int):
    global cars
    car = get_car(id)
    if car is None:
        return jsonify(
            {
                'error': 'car does not exist'
            },
            404
        )
    car = [i for i in cars if i['id'] != id]
    return jsonify(car), 200

app.run()
