import datetime
import json
import time

from decouple import config
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import utils


@csrf_exempt
def aisles(request, slug=None):
    if request.method == "POST":
        # Verifica a API Key e encontra o respectivo cliente
        api_key = request.headers.get('X-Api-Key')
        if not api_key:
            return JsonResponse({'error': f"Header faltando: 'X-Api-Key'"}, status=400)
        client_id = utils.find_client_by_api_key(api_key)
        if client_id is None:
            return JsonResponse({'error': 'API Key invalida'}, status=401)
        # Encontra os corredores a serem retornados
        results = utils.get_corredores(slug)
        return JsonResponse(results, safe=False, status=200)
    return JsonResponse({"error": "Metodo de requisicao invalido"}, status=405)


@csrf_exempt
def bulk_update(request):
    if request.method == "POST":
        # Verifica o header 'Content-Type' da requisição
        content_type = request.headers.get('Content-Type')
        if not content_type or content_type != "application/json":
            return JsonResponse({'error': f"Header faltando ou invalido: 'Content-Type'"}, status=400)
        # Verifica a API Key e encontra o respectivo cliente
        api_key = request.headers.get('X-Api-Key')
        if not api_key:
            return JsonResponse({'error': f"Header faltando: 'X-Api-Key'"}, status=400)
        client_id = utils.find_client_by_api_key(api_key)
        if client_id is None:
            return JsonResponse({'error': 'API Key invalida'}, status=401)
        # Verifica o 'body' da requisição e aplica os dados da requisição no banco de dados
        try:
            payload = json.loads(request.body)
            try:
                if isinstance(payload["loja_id"], float):
                    return JsonResponse({'error': f"Campo invalido: 'loja_id'"}, status=400)
                client_shop_id = int(payload["loja_id"])
                if not 0 <= client_shop_id <= 2147483647:
                    return JsonResponse({'error': f"Campo invalido: 'loja_id'"}, status=400)
            except (KeyError, TypeError) as e:
                return JsonResponse({'error': f"Campo faltando ou invalido: 'loja_id'"}, status=400)
            try:
                produtos = payload["produtos"]
            except KeyError:
                return JsonResponse({'error': f"Campo faltando ou invalido: 'produtos'"}, status=400)
            if utils.bulk_update(client_id, client_shop_id, produtos) == 0:
                return JsonResponse({"status": "success"}, status=200)
            else:
                return JsonResponse({'error': f"Parametros invalidos"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON invalido"}, status=400)
        
    return JsonResponse({"error": "Metodo de requisicao invalido"}, status=405)


@csrf_exempt
def categories(request, slug=None):
    if request.method == "POST":
        # Verifica a API Key e encontra o respectivo cliente
        api_key = request.headers.get('X-Api-Key')
        if not api_key:
            return JsonResponse({'error': f"Header faltando: 'X-Api-Key'"}, status=400)
        client_id = utils.find_client_by_api_key(api_key)
        if client_id is None:
            return JsonResponse({'error': 'API Key invalida'}, status=401)
        # Verifica o 'body' da requisição e encontra as categorias a serem retornadas
        try:
            payload = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalido'}, status=400)
        loja_id = payload.get("loja_id", None)
        results = utils.get_categorias(slug=slug, client_id=client_id, client_shop_id=loja_id)
        return JsonResponse(results, safe=False, status=200, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({"error": "Metodo de requisicao invalido"}, status=405)


@csrf_exempt
def generate_api_key(request):
    if request.method == "POST":
        # Verifica o 'body' da requisição e gera a chave API a ser retornada
        try:
            payload = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalido'}, status=400)
        nome_cliente = payload.get("nome_cliente")
        if nome_cliente is None:
            return JsonResponse({'error': f"Campo faltando: 'nome_cliente'"}, status=400)
        api_key = utils.generate_api_key(nome_cliente)
        return JsonResponse({"api_key": api_key}, status=200)
    return JsonResponse({"error": "Metodo de requisicao invalido"}, status=405)


@csrf_exempt
def search(request):

    # Lida com requisição OPTIONS - CORS preflight
    if request.method == 'OPTIONS':
        response = JsonResponse({'message': 'CORS preflight response'})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'X-Api-Key, Content-Type, Authorization'
        return response

    # Lida com requisição POST
    if request.method == 'POST':
        # Recolhe a data/hora da requisição
        request_timestamp = datetime.datetime.fromtimestamp(time.time())
        # Verifica o header 'Content-Type' da requisição
        content_type = request.headers.get('Content-Type')
        if not content_type or content_type != 'application/json':
            return JsonResponse({'error': f"Header faltando ou invalido: 'Content-Type'"}, status=400)
        # Verifica a API Key e encontra o respectivo cliente
        api_key = request.headers.get('X-Api-Key')
        if not api_key:
            return JsonResponse({'error': f"Header faltando: 'X-Api-Key'"}, status=400)
        client_id = utils.find_client_by_api_key(api_key)
        if client_id is None:
            return JsonResponse({'error': 'API Key invalida'}, status=401)         
        # Verifica 'body' da requisição
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalido'}, status=400)
        q = payload.get("q")
        if q is None:
            return JsonResponse({'error': f"Campo faltando: 'q'"}, status=400)
        results_per_page = payload.get("resultados_por_pagina", 48)
        try:
            results_per_page = int(results_per_page)
            if not 1 <= results_per_page <= 1000:
                return JsonResponse({'error': f"Campo invalido: 'resultados_por_pagina'"}, status=400)
        except TypeError:
            return JsonResponse({'error': f"Campo invalido: 'resultados_por_pagina'"}, status=400)
        page_number = payload.get("numero_pagina", 1)
        try:
            page_number = int(page_number)
            if page_number <= 0:
                return JsonResponse({'error': f"Campo invalido: 'numero_pagina'"}, status=400)
        except TypeError:
            return JsonResponse({'error': f"Campo invalido: 'numero_pagina'"}, status=400)
        client_shop_id = payload.get("loja_id")
        if client_shop_id:
            try:
                client_shop_id = int(client_shop_id)
                if not 0 <= client_shop_id <= 2147483647:
                    return JsonResponse({'error': f"Campo invalido: 'loja_id'"}, status=400)
            except TypeError:
                return JsonResponse({'error': f"Campo faltando ou invalido: 'loja_id'"}, status=400)
        # Gera a lista de resultados para o termo de pesquisa
        results = utils.pesquisa(q, results_per_page, page_number, client_id, client_shop_id, request_timestamp)
        return JsonResponse(results, safe=False, status=200)
    return JsonResponse({'error': 'Metodo de requisicao invalido'}, status=405)
