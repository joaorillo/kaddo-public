# Real code omitted for security reasons

import re
import time

import psycopg2
import pytest
from decouple import config
from django.conf import settings
from django.core.management.base import BaseCommand

from search_api import utils
from search_api.management.commands import pre_cadastro_rotina
from search_api.management.preprocessing_utils import create_db, errors_testes


class Command(BaseCommand):
    help = "Creates database"

    def add_arguments(self, parser):
        parser.add_argument(
            "kaddo_shop_id_preprocessing",
            type=int,
            nargs="?",
            default=0,
            help="kaddo_shop_id I want to run preprocessing on",
        )
        parser.add_argument(
            "--start",
            type=int,
            default=1,
            help="Step to start running preprocessing on",
        )

    def handle(self, *args, **options):
        kaddo_shop_id_preprocessing = options["kaddo_shop_id_preprocessing"]
        start = options["start"]
        preprocessing(kaddo_shop_id_preprocessing, start)


def preprocessing(kaddo_shop_id_preprocessing, start):
    pass