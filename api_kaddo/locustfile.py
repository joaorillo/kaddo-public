import json

from decouple import config
from locust import HttpUser, between, task

api_key = config("SERVER_API_KEY")


class ApiUser(HttpUser):
    wait_time = between(0.01, 0.02)


    @task
    def search(self):

        data_search = {"q": "ketchup hellmanns", "loja_id": 200}
        headers_search = {"Content-Type": "application/json", "X-Api-Key": api_key}
        response_search = self.client.post("/search_api/search/", json=data, headers=headers_search)
        print(f"response_search: {response_search.json()}")

        data_bulk_update = {
            "loja_id": 200,
            "produtos": [
                {"ean": 9999999999999, "nome_produto": "maionese hellmann's 2kg", "disponivel": 'N',},
                {"ean": 115, "nome_produto": "Ketchup picante 380g Hellmann's", "disponivel": 0,},
                {"ean": 9999999999996, "nome_produto": "creme de avelã nutella 1kg", "disponivel": 'yes',},
                {"ean": 9999999999995, "nome_produto": "chocolate ao leite lacta 250g", "disponivel": 'no',},
            ]
        }
        headers_bulk_update = {
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
        }
        response_bulk_update = self.client.post("/search_api/bulk_update/", json=data, headers=headers_bulk_update)
        print(f"response_bulk_update: {response_bulk_update.json()}")
