from typing import List, Dict, Union

class Dashboard():
    def __init__(
            self,
            articles_per_year: List[Dict[str, str]] = None,
            articles_per_stratum: List[Dict[str, str]] = None,
            articles_per_field: List[Dict[str, int]] = None,
            authors_with_supervision_count: List[Dict[str, Union[str, int]]] = None):

        self.__articles_per_year = articles_per_year
        self.__articles_per_stratum = articles_per_stratum
        self.__articles_per_field = articles_per_field
        self.__authors_with_supervision_count = authors_with_supervision_count
    
    @property
    def articles_per_year(self):
        return self.__articles_per_year

    @property
    def articles_per_stratum(self):
        return self.__articles_per_stratum

    @property
    def articles_per_field(self):
        return self.__articles_per_field
    
    @property
    def authors_with_supervision_count(self):
        return self.__authors_with_supervision_count