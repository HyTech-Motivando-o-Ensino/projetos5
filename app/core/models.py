from django.db import models


class ArquivoXml(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    payload = models.TextField(blank=True, null=True)
    status_extracao = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'arquivos_xml'


class Artigo(models.Model):
    natureza = models.CharField(max_length=255, blank=True, null=True)
    titulo = models.CharField(max_length=500, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    idioma = models.CharField(max_length=100, blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True)
    periodico_revista_issn = models.CharField(max_length=100, blank=True, null=True)
    sequencia_producao = models.IntegerField(blank=True, null=True)
    pdf_file = models.CharField(max_length=100, blank=True, null=True)
    areas_conhecimento = models.ManyToManyField('GrandeAreaConhecimento', through='ArtigoAreaConhecimento')

    class Meta:
        managed = True
        db_table = 'artigos'


class GrandeAreaConhecimento(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'grande_area_conhecimento'


class ArtigoAreaConhecimento(models.Model):
    area_conhecimento = models.ForeignKey('GrandeAreaConhecimento', models.CASCADE)
    artigo = models.ForeignKey('Artigo', models.CASCADE)

    class Meta:
        managed = True
        db_table = 'artigo_area_conhecimento'
        unique_together = (('area_conhecimento', 'artigo'),)


class Autor(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    nome_completo = models.CharField(max_length=255, blank=True, null=True)
    resumo_cv = models.TextField(blank=True, null=True)
    colaborador_cesar = models.IntegerField(blank=True, null=True)
    areas_conhecimento = models.ManyToManyField('GrandeAreaConhecimento', through='AutorAreaConhecimento')
    artigos = models.ManyToManyField('Artigo', through='AutorArtigo')

    class Meta:
        managed = True
        db_table = 'autores'


class AutorAreaConhecimento(models.Model):
    autor = models.ForeignKey(Autor, models.CASCADE)
    area_conhecimento = models.ForeignKey('GrandeAreaConhecimento', models.CASCADE)

    class Meta:
        managed = True
        db_table = 'autores_area_conhecimento'
        unique_together = (('autor', 'area_conhecimento'),)


class AutorArtigo(models.Model):
    autor = models.ForeignKey(Autor, models.CASCADE)
    artigo = models.ForeignKey(Artigo, models.CASCADE)

    class Meta:
        managed = True
        db_table = 'autores_artigos'
        unique_together = (('autor', 'artigo'),)


class Curso(models.Model):
    nome = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cursos'

class Orientacao(models.Model):
    titulo = models.CharField(max_length=500, blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    natureza = models.CharField(max_length=100, blank=True, null=True)
    curso = models.CharField(max_length=200, blank=True, null=True)
    instituicao = models.CharField(max_length=200, blank=True, null=True)
    orientador = models.ForeignKey(Autor, models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orientacoes'


class OrientacaoAreaConhecimento(models.Model):
    orientacao_id = models.ForeignKey(Orientacao, models.CASCADE, blank=True, null=True)
    area_conhecimento_id = models.ForeignKey(GrandeAreaConhecimento, models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orientacao_area_conhecimento'
        unique_together = (('orientacao_id', 'area_conhecimento_id'),)




class PeriodicosRevistas(models.Model):
    issn = models.CharField(max_length=100, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)
    estrato = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'periodicos_revistas'
