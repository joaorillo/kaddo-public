# API Kaddô
Single-app project in Django

## Overview

One of the solutions developped by us at Kaddô is an API specialized in supermarket e-commerce. This repository is
a copy of the original project with the same structure, but sensitive parts have been ommited.

A key feature of our API is the 'Search Endpoint', designed to address the challenge of finding grocery items through
the search engine. Given a search term, it returns the best results in an optimized order and filtered appropriately. This
solution is presented at [this presentation](./media/apresentacao_kaddo_pesquisa.pdf).

Also, on a collaborative project that uses this exact endpoint, we've developped an innovative interface
(patent request pending) which is presented at [this presentation](./media/apresentacao_kaddo_interface.pdf)
and can be explored at [Kaddô - Interface](https://www.kaddo.com.br/interface).

Unfortunately, since most of the code is secret and therefore is omitted, the project can't be tested locally, but
you can have an idea of how it is structured.

## Documentation

You can check the documentation for the 'real' API at the following link:
[API Documentation](https://www.documenter.getpostman.com/view/36955707/2sA3kSo3Uo). Here, you can explore the actual
results we provide to our clients.

Additionally, you can refer to [`/media/fluxogram_api_kaddo.pdf`](./media/fluxogram_api_kaddo.pdf) for a basic flowchart of this API.

## Solutions

The most innovative and technically challenging solutions created include:
- An algorithm that automatically registers new products, inferring relevant information such as brand and category
based solely on the product's name
- A search engine algorithm specialized on supermarket items, which effectively addresses the problem of not finding 
desired products
- An innovative interface/methodology (patent pending) which uses this API's Search Endpoint

You can try the following query examples to test our algorithm by querying the Search Endpoint and comparing the
results (items) to any Brazilian supermarket's e-commerce search engine. I strongly encourage you to also test these
same queries at our interface ([Kaddô Interface](https://www.kaddo.com.br/interface)) and notice the difference in
how easy it is to choose products on both of them:
- "Leite"
- "Papel higiênico"
- "Café"
- "Nescau"
- "Achocolatado líquido"
- "Saco de lixo azul"
- "Desodorante feminino"
- "Chocolate barra"

## Initial setup

```
This project can't be run, since crucial parts of it are omitted for security reasons.
You can see the 'real' results of the API by following it documentation above.
```

## Project structure

### Search API (single-app)
TODO
