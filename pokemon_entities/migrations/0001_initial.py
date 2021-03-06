# Generated by Django 2.2.3 on 2019-07-31 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(max_length=200)),
                ('title_en', models.CharField(blank=True, max_length=200)),
                ('title_jp', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='pokemons')),
                ('next_evolution', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_evolution', to='pokemon_entities.Pokemon')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('appeared_at', models.DateTimeField(default=None)),
                ('dissapeared_at', models.DateTimeField(default=None)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('health', models.IntegerField(blank=True, null=True)),
                ('strength', models.IntegerField(blank=True, null=True)),
                ('defence', models.IntegerField(blank=True, null=True)),
                ('stamina', models.IntegerField(blank=True, null=True)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.Pokemon')),
            ],
        ),
    ]
