from google.cloud import datastore
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais.json"


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api",methods=["POST"])
def register_new_car():
    try:
        datastore_client = datastore.Client()
    except:
        return jsonify(isError=True,
                       message="Erro ao tentar iniciar cliente no datastore",
                       statusCode=500,
                       data='Erro ao tentar iniciar cliente no datastore'), 500

    # o tipo da entidade
    type = 'Carro'
    # o nome/id da entidade
    car_plate = request.json.get('car_plate')
    # Cloud Datastore key
    car_key = datastore_client.key(type, car_plate)

    # Criação da entidade
    car = datastore.Entity(key=car_key)
    car['color'] = request.json.get('color')
    car['price'] = request.json.get('price')
    car['model'] = request.json.get('model')
    car['brand'] = request.json.get('brand')
    car['car_plate'] = car_plate

    # Salva a entidade
    datastore_client.put(car)

    # printa o resultado
    print('Salvando carro {}: {}'.format(car.key.name, car['model']))

    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   data='Veículo cadastrado com sucesso'), 200
@app.route("/get",methods=["POST"])
def get_carro():
    try:
        client = datastore.Client()
    except:
        return jsonify(isError=True,
                       message="Erro ao tentar iniciar cliente no datastore",
                       statusCode=500,
                       data='Erro ao tentar iniciar cliente no datastore'), 500

    query = client.query(kind='Carro')
    query.add_filter('car_plate', '=', request.json.get('car_plate'))
    results = list(query.fetch())
    return jsonify(isError=False,
                   message="Dados Encontrados!",
                   statusCode=200,
                   data=results), 200

if __name__ == '__main__':
    app.run(debug=True)
