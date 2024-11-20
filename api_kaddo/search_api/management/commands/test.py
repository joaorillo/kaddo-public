import pytest
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Realiza todos os testes do app"

    def handle(self, *args, **options):
        test()


def test():

    result = pytest.main(['search_api/test'])
    return result
