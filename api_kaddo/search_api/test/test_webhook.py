import json

import psycopg2
import requests
from decouple import config

from search_api.management.commands import pre_cadastro_rotina

BASE_URL = "http://localhost:8000/search_api/bulk_update/"
BASE_API_KEY = config("KADDO_API_KEY_LOCAL")
BASE_HEADERS = {"Content-Type": "application/json", "X-Api-Key": BASE_API_KEY}


class TestWebhookResponseStatus:

    # Testa status code 200
    def test_webhook_status200(self):
        data = {
            "loja_id": 199,
            "produtos": [
                {
                    "ean": 9999999999999,
                    "nome_produto": "Maionese Hellmann's 2kg",
                    "disponivel": 1,
                },
                {
                    "ean": 9999999999998,
                    "nome_produto": "Ketchup Hellmann's 2kg",
                    "disponivel": 0,
                }
            ]
        }
        json_data = json.dumps(data)
        response = requests.post(BASE_URL, headers=BASE_HEADERS, data=json_data)
        assert response.status_code == 200

    # Testa status code 400
    def test_webhook_status400(self):

        ## Testa requisição header 'Content-Type' faltando ou inválido
        data = {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]}
        wrong_headers = [
            {"X-Api-Key": BASE_API_KEY},
            {"Content-Type": "application/x-www-form-urlencoded", "X-Api-Key": BASE_API_KEY},
            {},
        ]
        for headers in wrong_headers:
            response = requests.post(BASE_URL, headers=headers, data=data)
            assert response.status_code == 400

        ## Testa requisição com algum dos 'headers' faltando
        data = {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]}
        wrong_headers = [
            {"Content-Type": "application/json"},
            {"X-Api-Key": BASE_API_KEY},
            {},
        ]
        for headers in wrong_headers:
            response = requests.post(BASE_URL, headers=headers, data=data)
            assert response.status_code == 400

        ## Testa requisição com Json inválido
        wrong_data = [
            {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 199, "produtos": [{"ean": 9999999999998, "nome_produto": "Ketchup Hellmann's 2kg", "disponivel": 0,},]},
            {1: 199, "produtos": [{"ean": 9999999999998, "nome_produto": "Ketchup Hellmann's 2kg", "disponivel": 0,},]},
        ]
        for data in wrong_data:
            response = requests.post(BASE_URL, headers=BASE_HEADERS, data=data)
            assert response.status_code == 400

        ## Testa requisição com algum dos parâmetros necessários do 'body' faltando ou inválido
        wrong_data = [
            {"produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": -1, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 1.5, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 'abc', "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 199},
            {"loja_id": 199, "produtos": [{"nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 199, "produtos": [{"ean": 0, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 199, "produtos": [{"ean": -1, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 199, "produtos": [{"ean": 2.99, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 199, "produtos": [{"ean": 'abc', "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]},
            {"loja_id": 199, "produtos": [{"ean": 9999999999999, "disponivel": 1,},]},
            {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": -1,},]},
            {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1.6,},]},
            {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 'abc',},]},
            {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 'tr',},]},
            {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 'yy',},]},
        ]
        for data in wrong_data:
            response = requests.post(BASE_URL, headers=BASE_HEADERS, data=data)
            assert response.status_code == 400

    # Testa status code 401
    def test_webhook_status401(self):
        ## Testa requisição com API Key errada
        data = {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]}
        wrong_headers = {"Content-Type": "application/json",  "X-Api-Key": 'wrong-key'}
        response = requests.post(BASE_URL, headers=wrong_headers, data=data)
        assert response.status_code == 401

    # Testa status code 405
    def test_webhook_status405(self):
        ## Testa requisições com métodos errados
        data = {"loja_id": 199, "produtos": [{"ean": 9999999999999, "nome_produto": "Maionese Hellmann's 2kg", "disponivel": 1,},]}
        response_get = requests.get(BASE_URL,)
        response_put = requests.put(
            BASE_URL,
            headers=BASE_HEADERS,
            data=data
        )
        response_delete = requests.delete(BASE_URL,)
        response_patch = requests.patch(
            BASE_URL,
            headers=BASE_HEADERS,
            data=data
        )
        response_head = requests.head(BASE_URL,)
        response_options = requests.options(BASE_URL,)
        wrong_method_responses = [
            response_get,
            response_put,
            response_delete,
            response_patch,
            response_head,
            response_options,
        ]
        for response in wrong_method_responses:
            assert response.status_code == 405


# Código real omitido
class TestWebhookWorking:
    pass