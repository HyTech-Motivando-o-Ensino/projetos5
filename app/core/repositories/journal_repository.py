from typing import List
from core.models import PeriodicosRevistas

class JournalRepository():
    def get_all(self) -> List[PeriodicosRevistas]:
        results = PeriodicosRevistas.objects.all()
        return results
    
    def get_all_issn(self) -> List[str]:
        results = PeriodicosRevistas.objects.values('issn')
        all_issn = [journal['issn'] for journal in results]
        return all_issn
