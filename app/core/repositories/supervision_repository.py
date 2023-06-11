from typing import Dict, List
from django.db.models import Count

from core.models import Orientacao

class SupervisionRepository():
    def get_all(self):
        return Orientacao.objects.all()

    def get_all_count(self, filter):
        data = Orientacao.objects.filter(filter).count()
        return data
