# Generated by Django 4.2.2 on 2023-06-08 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArquivoXml',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('payload', models.TextField(blank=True, null=True)),
                ('status_extracao', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'arquivos_xml',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Artigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('natureza', models.CharField(blank=True, max_length=255, null=True)),
                ('titulo', models.CharField(blank=True, max_length=500, null=True)),
                ('ano', models.IntegerField(blank=True, null=True)),
                ('idioma', models.CharField(blank=True, max_length=100, null=True)),
                ('doi', models.CharField(blank=True, max_length=100, null=True)),
                ('periodico_revista_issn', models.CharField(blank=True, max_length=100, null=True)),
                ('sequencia_producao', models.IntegerField(blank=True, null=True)),
                ('pdf_file', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'artigos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('nome_completo', models.CharField(blank=True, max_length=255, null=True)),
                ('resumo_cv', models.TextField(blank=True, null=True)),
                ('colaborador_cesar', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'autores',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
            options={
                'db_table': 'cursos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GrandeAreaConhecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'grande_area_conhecimento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Orientacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=500, null=True)),
                ('ano', models.IntegerField(blank=True, null=True)),
                ('natureza', models.CharField(blank=True, max_length=100, null=True)),
                ('curso', models.CharField(blank=True, max_length=200, null=True)),
                ('instituicao', models.CharField(blank=True, max_length=200, null=True)),
                ('orientador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.autor')),
            ],
            options={
                'db_table': 'orientacoes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PeriodicosRevistas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issn', models.CharField(blank=True, max_length=100, null=True)),
                ('nome', models.CharField(blank=True, max_length=255, null=True)),
                ('estrato', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'periodicos_revistas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AutorArtigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.artigo')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.autor')),
            ],
            options={
                'db_table': 'autores_artigos',
                'managed': True,
                'unique_together': {('autor', 'artigo')},
            },
        ),
        migrations.CreateModel(
            name='AutorAreaConhecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_conhecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.grandeareaconhecimento')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.autor')),
            ],
            options={
                'db_table': 'autores_area_conhecimento',
                'managed': True,
                'unique_together': {('autor', 'area_conhecimento')},
            },
        ),
        migrations.AddField(
            model_name='autor',
            name='areas_conhecimento',
            field=models.ManyToManyField(through='core.AutorAreaConhecimento', to='core.grandeareaconhecimento'),
        ),
        migrations.AddField(
            model_name='autor',
            name='artigos',
            field=models.ManyToManyField(through='core.AutorArtigo', to='core.artigo'),
        ),
        migrations.CreateModel(
            name='ArtigoAreaConhecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_conhecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.grandeareaconhecimento')),
                ('artigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.artigo')),
            ],
            options={
                'db_table': 'artigo_area_conhecimento',
                'managed': True,
                'unique_together': {('area_conhecimento', 'artigo')},
            },
        ),
        migrations.AddField(
            model_name='artigo',
            name='areas_conhecimento',
            field=models.ManyToManyField(through='core.ArtigoAreaConhecimento', to='core.grandeareaconhecimento'),
        ),
        migrations.CreateModel(
            name='OrientacaoAreaConhecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_conhecimento_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.grandeareaconhecimento')),
                ('orientacao_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.orientacao')),
            ],
            options={
                'db_table': 'orientacao_area_conhecimento',
                'managed': True,
                'unique_together': {('orientacao_id', 'area_conhecimento_id')},
            },
        ),
    ]
