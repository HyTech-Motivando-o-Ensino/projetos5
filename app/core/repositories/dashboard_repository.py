from core.entities import Dashboard
from .article_repository import ArticleRepository
from .knowledge_field_repository import KnowledgeFieldRepository
from .author_repository import AuthorRepository


class DashboardRepository():
    def __init__(self):
        self.__article_repository = ArticleRepository()
        self.__knowledge_field_repository = KnowledgeFieldRepository()
        self.__author_repository = AuthorRepository()
    
    def get_dashboard_data(self) -> Dashboard:
        articles_per_year = self.__article_repository.get_by_year()
        articles_per_stratum = self.__article_repository.get_by_stratum()
        knowledge_field_article_count = self.__knowledge_field_repository.get_all_group_by_articles()
        authors_with_supervision_count = self.__author_repository.get_all_with_clustered_supervision_count()

        return Dashboard(
            articles_per_year=articles_per_year,
            articles_per_stratum=articles_per_stratum,
            articles_per_field=knowledge_field_article_count,
            authors_with_supervision_count=authors_with_supervision_count)
