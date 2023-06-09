from django.db.models import Count
from typing import List, Dict

from core.models import Artigo

class ArticleRepository():
    def get_all(self):
        data = Artigo.objects.all()
        return data
    
    def get_all_count(self, filter):
        data = Artigo.objects.filter(filter).count()
        return data
    
    def get_by_year(self) -> List[Dict[str, str]]:
        data = Artigo.objects.values('ano').annotate(Count('ano')).order_by('ano')
        articles_per_year = [{'ano': article['ano'], 'count': article['ano__count']} for article in data]
        return articles_per_year
    
    def get_by_stratum(self) -> List[Dict[str, str]]:
        results = Artigo.objects.raw('''
            SELECT 1 as id, COUNT(*) as count, pr.estrato FROM artigos a
            INNER JOIN periodicos_revistas pr
            ON pr.issn = a.periodico_revista_issn
            GROUP BY pr.estrato
            ORDER BY pr.estrato;
        ''')

        articles_by_stratum = []
        for result in results:
            articles_by_stratum.append({'estrato': result.estrato, 'count': result.count})

        return articles_by_stratum
    
