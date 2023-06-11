from datetime import datetime
from django.db.models import Q
from django.db import connection

from core.entities import Dashboard
from .article_repository import ArticleRepository
from .knowledge_field_repository import KnowledgeFieldRepository
from .author_repository import AuthorRepository
from .supervision_repository import SupervisionRepository


class DashboardRepository():
    def __init__(self):
        self.__article_repository = ArticleRepository()
        self.__knowledge_field_repository = KnowledgeFieldRepository()
        self.__author_repository = AuthorRepository()
        self.__supervision_repository = SupervisionRepository()
    
    def get_dashboard_data(self) -> Dashboard:
        current_year = datetime.now().year
        triennium = [current_year - i for i in range(3)]
        
        articles_in_last_triennium = self.__article_repository.get_all_count(Q(ano__in=triennium))
        supervisions_in_last_triennium = self.__supervision_repository.get_all_count(Q(ano__in=triennium))
        articles_per_year = self.__article_repository.get_by_year()
        articles_per_stratum = self.__article_repository.get_by_stratum()
        total_articles = self.__article_repository.get_all_count(Q())
        knowledge_field_article_count = self.__knowledge_field_repository.get_all_group_by_articles()
        authors_with_supervision_count = self.__author_repository.get_all_with_clustered_supervision_count()

        return Dashboard(
            articles_in_last_triennium=articles_in_last_triennium,
            supervisions_in_last_triennium=supervisions_in_last_triennium,
            total_articles=total_articles,
            articles_per_year=articles_per_year,
            articles_per_stratum=articles_per_stratum,
            articles_per_field=knowledge_field_article_count,
            authors_with_supervision_count=authors_with_supervision_count)
    
    def _calculate_publication_productivity_indicator(self):
        STRATUM_WEIGHTS = {
            'A1': 1,
            'A2': 0.875,
            'A3': 0.75,
            'B1': 0.625,
            'B2': 0.5,
            'B3': 0.375,
            'B4': 0.25,
            'B5': 0.125
        }

        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT
                    aut.nome_completo,
                    pr.estrato, art.ano,
                    COUNT(pr.estrato) as 'pub_count'
                FROM autores aut
                INNER JOIN autores_artigos aa
                ON aut.id = aa.autor_id 
                INNER JOIN artigos art
                ON art.id = aa.artigo_id
                INNER JOIN periodicos_revistas pr
                ON art.periodico_revista_issn = pr.issn
                WHERE pr.estrato != 'C'
                GROUP BY aut.nome_completo, pr.estrato, art.ano
                ORDER BY aut.nome_completo;
            ''')
            instances = cursor.fetchall()
    
        data_points_by_author = {}
        # {'cesar franca': { 2020: [], 2021: [] }, ...} 
        for instance in instances:
            stratum = instance[1]
            if stratum in STRATUM_WEIGHTS:
                full_name = instance[0]
                year = instance[2]
                count = instance[3]

                if full_name not in data_points_by_author:
                    data_points_by_author[full_name] = {}

                if year not in data_points_by_author[full_name]:
                    data_points_by_author[full_name][year] = []

                data_points_by_author[full_name][year].append(STRATUM_WEIGHTS[stratum] * count)
        