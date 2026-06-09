# Importando as bibliotecas necessárias
from flask import Flask, request, jsonify
import joblib
import numpy as np

# Inicializando a aplicação Flask
app = Flask(__name__)

# Carregando os modelos treinados
modelo_classificacao = joblib.load('modelo_classificacao.pkl')
modelo_regressao = joblib.load('modelo_regressao.pkl')

# Endpoint 1: Previsão de Risco de Tsunami

@app.route('/predict/risco', methods=['POST'])
def prever_risco():
    dados = request.get_json()

    features = [[
        dados['magnitude'],
        dados['depth'],
        dados['latitude'],
        dados['longitude'],
        dados['gap'],
        dados['dmin'],
        dados['sig']
    ]]

    resultado = modelo_classificacao.predict(features)[0]
    risco = 'Tsunami' if resultado == 1 else 'Sem Tsunami'

    return jsonify({
        'risco': risco,
        'codigo': int(resultado)
    })

# Endpoint 2: Previsão de Temperatura do Mar

@app.route('/predict/temperatura', methods=['POST'])
def prever_temperatura():
    dados = request.get_json()

    features = [[
        dados['latitude'],
        dados['longitude'],
        dados['ph_level'],
        dados['species_observed'],
        dados['marine_heatwave']
    ]]

    temperatura = modelo_regressao.predict(features)[0]

    return jsonify({
        'temperatura_prevista': round(float(temperatura), 2),
        'unidade': 'Celsius'
    })


# Rota principal — verifica se a API está online

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'online',
        'projeto': 'DeepScan',
        'endpoints': ['/predict/risco', '/predict/temperatura']
    })

# Iniciando o servidor
if __name__ == '__main__':
    app.run(debug=True)