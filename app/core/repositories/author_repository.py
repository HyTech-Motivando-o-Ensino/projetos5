from typing import List, Dict, Union
from django.db.models import Count
from operator import itemgetter

from core.models import Autor

class AuthorRepository():
    def get_all(self) -> List[Autor]:
        results = Autor.objects.all()
        return results

    def get_all_count(self, filter):
        data = Autor.objects.filter(filter).count()
        return data
    
    def get_all_with_supervision_count(self) -> List[Dict[str, int]]:
        results = Autor.objects.all() \
            .prefetch_related('orientacoes') \
            .annotate(count=Count('orientacoes')) \
            .order_by('-count')

        return self._convert_instances_to_dashboard(results)
    
    def get_all_with_clustered_supervision_count(self) -> List[Dict[str, Union[str, int]]]:
        results = Autor.objects.values(
            "nome_completo", "orientacoes__natureza"
        ).order_by().annotate(count=Count("orientacoes__natureza"))

        return self._convert_clustered_instances_to_dashboard(results)
    

    def _convert_instances_to_dashboard(self, instances) -> List[Dict[str, int]]:
        return [{'nome': instance.nome_completo, 'count': instance.count} for instance in instances]

    def _convert_clustered_instances_to_dashboard(self, instances) -> List[Dict[str, Union[str, int]]]:
        FILTERED_SUPERVISIONS = [
            "trabalho_conclusao_graduacao",
            "dissertacao_mestrado",
            "tese_doutorado",
            "trabalho_iniciacao_cientifica"]

        authors_dict = {}
        # {'erico': {'dissertacao de mestrado': 12, 'tese de doutorado': 2}, ...}
        for instance in instances:
            name = instance['nome_completo']
            sup_type = instance['orientacoes__natureza']
            count = instance['count']

            if (sup_type in FILTERED_SUPERVISIONS and count > 0):
                if name not in authors_dict:
                    authors_dict[name] = {}
                    for supervision in FILTERED_SUPERVISIONS:
                        authors_dict[name][supervision] = 0

                authors_dict[name][sup_type] = count

        author_supervision_clusters = [{'nome_completo': author, **authors_dict[author]} for author in authors_dict]
        return sorted(author_supervision_clusters, key=lambda c: sum(itemgetter(*FILTERED_SUPERVISIONS)(c)), reverse=True)
