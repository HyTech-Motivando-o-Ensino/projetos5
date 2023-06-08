from core.entities import Dashboard
from .article_repository import ArticleRepository
from .journal_repository import JournalRepository


class DashboardRepository():
    def __init__(self, ):
        self.__article_repository = ArticleRepository()
    
    def get_dashboard_data(self):
        articles_per_year = self.__article_repository.get_by_year()
        articles_per_stratum = self.__article_repository.get_by_stratum()
        return Dashboard(
            articles_per_year=articles_per_year,
            articles_per_stratum=articles_per_stratum)