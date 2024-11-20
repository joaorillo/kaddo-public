import psycopg2
import requests
from decouple import config

from api import settings
from search_api import utils

BASE_URL = "http://localhost:8000/search_api/search/"
BASE_API_KEY = config("KADDO_API_KEY_LOCAL")
BASE_HEADERS = {"Content-Type": "application/json", "X-Api-Key": BASE_API_KEY,}


class TestAPIResponseStatus:

    # Testa status code 200
    def test_api_status200(self):
        ## Testa requisição correta
        correct_data = [
            {"q": "Ketchup Hellmann's", "numero_pagina": "1", "resultados_por_pagina": "15", "loja_id": 0},
            {"q": "Ketchup Hellmann's", "numero_pagina": "1", "loja_id": 0},
            {"q": "Ketchup Hellmann's", "resultados_por_pagina": "15", "loja_id": 0},
            {"q": "Ketchup Hellmann's", "loja_id": 0},
        ]
        for data in correct_data:
            response = requests.post(
                BASE_URL,
                headers=BASE_HEADERS,
                json=data
            )
        assert response.status_code == 200

    # Testa status code 400
    def test_api_status400(self):

        ## Testa requisição com header 'Content-Type' inválido
        data = {"q": "Maionese Hellmann's", "numero_pagina": "1", "resultados_por_pagina": "15", "loja_id": 0}
        wrong_headers = [
            {"Content-Type": "application/xml", "X-Api-Key": BASE_API_KEY,},
        ]
        for headers in wrong_headers:
            response = requests.post(
                BASE_URL,
                headers=headers,
                json=data
            )
            assert response.status_code == 400

        ## Testa requisição com header 'X-Api-Key' faltando
        data = {"q": "Ketchup Hellmann's", "numero_pagina": "1", "resultados_por_pagina": "15", "loja_id": 0}
        wrong_headers = {"Content-Type": "application/json",}
        response = requests.post(BASE_URL, headers=wrong_headers, json=data)
        assert response.status_code == 400

        ## Testa requisição com algum dos parâmetros necessários do 'body' faltando
        wrong_data = [
            {"numero_pagina": "1", "resultados_por_pagina": "15", "loja_id": 0},
            {"numero_pagina": "1", "resultados_por_pagina": "15"},
            {},          
        ]
        for data in wrong_data:
            response = requests.post(
                BASE_URL,
                headers=BASE_HEADERS,
                json=data
            )
            assert response.status_code == 400

        ## Testa requisição com algum dos parâmetros inválido
        wrong_data = [
            {"q": "Ketchup Hellmann's", "loja_id": 'abc'},
            {"q": "Ketchup Hellmann's", "loja_id": 0},
            {"q": "Ketchup Hellmann's", "loja_id": -3},
            {"q": "Ketchup Hellmann's", "numero_pagina": 'abc', "loja_id": 'abc'},
            {"q": "Ketchup Hellmann's", "numero_pagina": -1, "loja_id": 0},
            {"q": "Ketchup Hellmann's", "numero_pagina": 0, "loja_id": -3},
            {"q": "Ketchup Hellmann's", "resultados_por_pagina": 'abc', "loja_id": 'abc'},
            {"q": "Ketchup Hellmann's", "resultados_por_pagina": -3, "loja_id": 0},
            {"q": "Ketchup Hellmann's", "resultados_por_pagina": 0, "loja_id": -3},
        ]
        for data in wrong_data:
            response = requests.post(BASE_URL, headers=wrong_headers, json=data)
            assert response.status_code == 400

    # Testa status code 401
    def test_api_status401(self):
        ## Testa requisição com API Key errada
        data = {"q": "Ketchup Hellmann's", "numero_pagina": "1", "resultados_por_pagina": "15", "loja_id": 0}
        wrong_headers = {"Content-Type": "application/json",  "X-Api-Key": 'wrong-key'}
        response = requests.post(BASE_URL, headers=wrong_headers, json=data)
        assert response.status_code == 401

    # Testa status code 405
    def test_api_status405(self):
        ## Testa requisições com métodos errados
        data = {"q": "Ketchup Hellmann's", "numero_pagina": "1", "resultados_por_pagina": "15", "loja_id": 0}
        response_get = requests.get(BASE_URL,)
        response_put = requests.put(
            BASE_URL,
            headers=BASE_HEADERS,
            json=data
        )
        response_delete = requests.delete(BASE_URL,)
        response_patch = requests.patch(
            BASE_URL,
            headers=BASE_HEADERS,
            json=data
        )
        response_head = requests.head(BASE_URL,)
        wrong_method_responses = [
            response_get,
            response_put,
            response_delete,
            response_patch,
            response_head,
        ]
        for response in wrong_method_responses:
            assert response.status_code == 405


# Código real omitido
class TestAPIResponseResults:
    pass
