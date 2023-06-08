from typing import List, Dict

class Dashboard():
    def __init__(
            self,
            articles_per_year: List[Dict[str, str]] = None,
            articles_per_stratum: List[Dict[str, str]] = None):

        self.__articles_per_year = articles_per_year
        self.__articles_per_stratum = articles_per_stratum
    
    @property
    def articles_per_year(self):
        return self.__articles_per_year

    @property
    def articles_per_stratum(self):
        return self.__articles_per_stratum