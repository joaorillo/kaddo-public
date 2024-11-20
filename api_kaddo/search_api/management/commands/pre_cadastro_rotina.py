# Real code omitted for security reasons

import psycopg2
from decouple import config
from django.conf import settings
from django.core.management.base import BaseCommand

from search_api import utils


class Command(BaseCommand):
    help = "Realiza todos os pré-cadastros necessários para uma determinada loja"

    def add_arguments(self, parser):
        parser.add_argument(
            "is_preprocessing",
            type=int,
            help="1 if preprocessing is calling; 0 otherwise",
        )
        ## -1 to run on all shops
        parser.add_argument(
            '--kaddo_shop_id', type=int, default=-1, help="shop I want to run pre_cadastro on"
        )

    def handle(self, *args, **options):
        is_preprocessing = options["is_preprocessing"]
        kaddo_shop_id = options["kaddo_shop_id"]
        pre_cadastro_rotina(is_preprocessing, kaddo_shop_id)


def pre_cadastro_rotina(is_preprocessing, kaddo_shop_id):
    pass
