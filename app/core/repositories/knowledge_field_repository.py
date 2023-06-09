from typing import Dict, List
from core.models import GrandeAreaConhecimento

class KnowledgeFieldRepository():
    def get_all(self):
        return GrandeAreaConhecimento.objects.all()
    
    def get_all_group_by_articles(self) -> List[Dict[str, int]]:
        results = GrandeAreaConhecimento.objects.all().prefetch_related('artigos')
        knowledge_field_group_by_articles = [
            {"label": instance.nome_formatado, "value": len(instance.artigos.all())}
            for instance in results if len(instance.artigos.all()) > 0]

        return knowledge_field_group_by_articles